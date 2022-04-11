from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Task(models.Model):
    CATEGORIES = (
        ('General', 'General'),
        ('Work', 'Work'),
        ('School', 'School')
    )
    task = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=10, choices=CATEGORIES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.task

    def get_absolute_url(self):
        return reverse('tasks')
