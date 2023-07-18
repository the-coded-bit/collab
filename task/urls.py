from django.urls import path
from . import views

urlpatterns = [
    path('get-tasks', views.get_tasks_by_id, name='get-tasks'),
    path('add-task', views.add_task, name='add-task'),
    path('complete-task', views.complete_task, name='complete-task'),
    path('notify-completed-task', views.notify_completed_tasks, name='notify-completed-tasks')
]