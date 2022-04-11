from django.shortcuts import render, reverse, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Task
from .forms import TaskForm


def home(request):
    # If user is logged in, user is redirected to their home page showing their tasks, instead of the sample task page.
    if request.user.is_authenticated:
        return redirect('tasks')
    return render(request, 'tasks/home.html')


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user).order_by('due_date')


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/new_task.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/new_task.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.owner


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete_task.html'

    def get_success_url(self):
        return reverse('tasks')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.owner
