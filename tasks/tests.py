import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import TaskForm
from .models import Task


class TaskTests(TestCase):
    username = 'fake_user123'
    pw = 'this1is2not3a4real5user@'

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
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        task_title = 'Clean the house'
        self.client.post(reverse('task-create'), data={
            'task': task_title,
            'category': 'General',
            'due_date': tomorrow
        })
        self.assertEqual(Task.objects.last().task, task_title)
