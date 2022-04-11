from django.urls import path
from . import views
from .views import TaskListView, TaskCreateView, TaskEditView, TaskDeleteView

urlpatterns = [
    path('', views.home, name='home'),
    path('mytasks/', TaskListView.as_view(), name='tasks'),
    path('new_task/', TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/update', TaskEditView.as_view(), name='task-edit'),
    path('task/<int:pk>/delete', TaskDeleteView.as_view(), name='task-delete')
]
