from django.urls import path
from .views import *

urlpatterns = [
    path('tasks/create/', CreateTaskView.as_view(), name='task_create'),
    path('tasks/', ReadTasksView.as_view(), name='task-list'),
    path('tasks/<int:task_id>/', EditTaskView.as_view(), name='task_detail')
]