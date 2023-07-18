from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    task_des = models.TextField()
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignee_tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_to_tasks')
    notify_status = models.BooleanField(default=False)
    isCompleted = models.BooleanField(default= False)
