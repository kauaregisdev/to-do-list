from django.urls import path
from .views import CreateTaskView, ReadTasksView, EditTaskView

urlpatterns = [
    path('tasks/', CreateTaskView.as_view(), name='task_create'),
    path('tasks/list/', ReadTasksView.as_view(), name='task_list'),
    path('tasks/<int:task_id>/', EditTaskView.as_view(), name='task_detail')
]