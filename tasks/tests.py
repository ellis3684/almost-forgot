import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import TaskForm
from .models import Task


class TaskTests(TestCase):
    username = 'fake_user123'
    pw = 'this1is2not3a4real5user@'
    task_title = 'Clean the house'
    category = 'General'
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(cls.username, password=cls.pw)

    def test_home_page_unauthenticated(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/home.html')

    def test_home_page_authenticated(self):
        self.client.login(username=self.username, password=self.pw)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))

    def test_create_task_valid(self):
        self.client.login(username=self.username, password=self.pw)
        self.client.post(reverse('task-create'), data={
            'task': self.task_title,
            'category': 'General',
            'due_date': self.tomorrow
        })
        self.assertEqual(Task.objects.last().task, self.task_title)

    def test_create_task_invalid_missing_task_title(self):
        self.client.login(username=self.username, password=self.pw)
        self.client.post(reverse('task-create'), data={
            'category': self.category,
            'due_date': self.tomorrow
        })
        self.assertEqual(Task.objects.all().count(), 0)

    def test_create_task_invalid_user_not_logged_in(self):
        self.client.post(reverse('task-create'), data={
            'task': self.task_title,
            'category': self.category,
            'due_date': self.tomorrow
        })
        self.assertEqual(Task.objects.all().count(), 0)

    def test_list_all_tasks(self):
        self.client.login(username=self.username, password=self.pw)
        task1 = Task.objects.create(
            task=self.task_title,
            category=self.category,
            due_date=self.tomorrow,
            owner=self.user
        )
        task2 = Task.objects.create(
            task='Submit timesheet',
            category='Work',
            due_date=self.tomorrow + datetime.timedelta(days=2),
            owner=self.user
        )
        response = self.client.get(reverse('tasks'))
        context_tasks = response.context['tasks']
        self.assertEqual(context_tasks[0].task, task1.task)
        self.assertEqual(context_tasks[1].task, task2.task)

    def test_list_tasks_empty(self):
        self.client.login(username=self.username, password=self.pw)
        response = self.client.get(reverse('tasks'))
        context_tasks = response.context['tasks']
        self.assertQuerysetEqual(context_tasks, [])
        self.assertContains(response, 'You have no tasks yet.')


