import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Task


class TaskTests(TestCase):
    # Create commonly used variables for TaskTests
    username = 'fake_user123'
    pw = 'this1is2not3a4real5user@'
    task_title = 'Clean the house'
    category = 'General'
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    @classmethod
    def setUpTestData(cls):
        """Create user in test database"""
        cls.user = User.objects.create_user(cls.username, password=cls.pw)

    def test_home_page_unauthenticated(self):
        """If user is anonymous/non-authenticated, 'home' url should use template 'home.html'"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/home.html')

    def test_home_page_authenticated(self):
        """If user is authenticated, 'home' url should redirect to 'tasks' url"""
        self.client.login(username=self.username, password=self.pw)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))

    def test_create_task_valid(self):
        """Creating a task via 'task-create' url should succeed"""
        self.client.login(username=self.username, password=self.pw)
        self.client.post(reverse('task-create'), data={
            'task': self.task_title,
            'category': 'General',
            'due_date': self.tomorrow
        })
        self.assertEqual(Task.objects.last().task, self.task_title)

    def test_create_task_invalid_missing_task_title(self):
        """Creating a task that does not include a task title fails to create a Task object in database"""
        self.client.login(username=self.username, password=self.pw)
        self.client.post(reverse('task-create'), data={
            'category': self.category,
            'due_date': self.tomorrow
        })
        self.assertEqual(Task.objects.all().count(), 0)

    def test_create_task_invalid_user_not_logged_in(self):
        """If user is not authenticated, task is not created"""
        self.client.post(reverse('task-create'), data={
            'task': self.task_title,
            'category': self.category,
            'due_date': self.tomorrow
        })
        self.assertEqual(Task.objects.all().count(), 0)

    def test_list_all_tasks(self):
        """'Tasks' url should list all currently existing Task objects for this user"""
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
        """If user has no tasks, none will be shown on 'tasks' url"""
        self.client.login(username=self.username, password=self.pw)
        response = self.client.get(reverse('tasks'))
        context_tasks = response.context['tasks']
        self.assertQuerysetEqual(context_tasks, [])
        self.assertContains(response, 'You have no tasks yet.')

    def test_edit_task_valid(self):
        """Edit task via 'task-edit' url should succeed"""
        new_task_title = 'Buy textbooks for upcoming semester'
        self.client.login(username=self.username, password=self.pw)
        task1 = Task.objects.create(task='This task is going to change', category='School', owner=self.user)
        response = self.client.post(reverse('task-edit', args=[task1.pk]), data={
            'task': new_task_title,
            'category': task1.category
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.last().task, new_task_title)

    def test_edit_task_missing_data(self):
        """If missing data Task model expects, task edit should fail"""
        self.client.login(username=self.username, password=self.pw)
        task1 = Task.objects.create(task='This task is going to change', category='School', owner=self.user)
        response = self.client.post(reverse('task-edit', args=[task1.pk]), data={
            'category': 'General'
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(Task.objects.last().category, 'General')

    def test_delete_task_success(self):
        """Delete task via 'task-delete' url should successfully delete"""
        self.client.login(username=self.username, password=self.pw)
        task1 = Task.objects.create(task='This is going to be deleted', category='General', owner=self.user)
        self.assertEqual(Task.objects.all().count(), 1)
        response = self.client.post(reverse('task-delete', args=[task1.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.all().count(), 0)

    def test_delete_non_existing_task(self):
        """Attempting to delete task with non-existing pk should fail with 404 error"""
        self.client.login(username=self.username, password=self.pw)
        response = self.client.post(reverse('task-delete', args=[3]))
        self.assertEqual(response.status_code, 404)
