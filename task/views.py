from django.http import HttpResponse, JsonResponse
from user.utils import ensure_valid_jwt
from .models import Task
from django.contrib.auth.models import User
import json
import jwt
from django.conf import settings
from user.utils import err_response
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

# Create your views here.
@ensure_valid_jwt
def get_tasks_by_id(request):
    if request.method == 'GET':
         token = request.get_signed_cookie('access-token', salt = settings.SECRET_KEY)
         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
         user = User.objects.get(id = payload['id'])
         assigned_tasks = Task.objects.filter(assigned_to = user)
         result_set = []
         for task in assigned_tasks:
                dict = model_to_dict(task)
                dict['assignee'] = {
                    'username': task.assignee.username,
                    'id': task.assignee.id,
                    'email': task.assignee.email
                }
                dict['assigned_to'] = {
                        'username': task.assigned_to.username,
                        'id': task.assigned_to.id,
                        'email': task.assigned_to.email
                    }
                result_set.append(dict)
         return JsonResponse({'response': result_set}, safe=False)
    else:
        return err_response('invalid request')

# endpoint to add task
@ensure_valid_jwt
def add_task(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        task_des = json_data['task_des']
        assignee = json_data['assignee']
        assigned_to = json_data['assigned_to']

        assignee_user = User.objects.get(id = assignee)
        assigned_to_user = User.objects.get(id = assigned_to)

        # Create a new task instance
        task = Task(task_des=task_des, assignee=assignee_user, assigned_to=assigned_to_user)
        task.save()

        # Return a JSON response indicating successful task creation
        return JsonResponse({'message': 'Task created successfully'})
    else:
        # Handle invalid request method
        return JsonResponse({'error': 'Invalid request method'}, status=405)


# endpoint to modify task status to complete
@ensure_valid_jwt
def complete_task(request):
     if request.method == 'GET':
        task_id = request.GET['id']
        task = get_object_or_404(Task, id=task_id)
        task.isCompleted = True
        task.notify_status = True
        task.save()

        return JsonResponse({'message': 'task added as complete'})
     else:
         return err_response('invalid request')
     
# endpoint to notify assignees about completed tasks
@ensure_valid_jwt
def notify_completed_tasks(request):
    if request.method == 'GET':
         token = request.get_signed_cookie('access-token', salt = settings.SECRET_KEY)
         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
         user = User.objects.get(id = payload['id'])
         assigned_tasks = Task.objects.filter(assignee = user, notify_status = True)
         tasks_list = [{'task_des': task.task_des, 'assigned_to': User.get_username(task.assigned_to)} for task in assigned_tasks]
         # Update the 'notify_status' of tasks to False
         for task in assigned_tasks:
            task.notify_status = False
            task.save()
         return JsonResponse({'response': tasks_list, 'count': tasks_list.__len__()}, safe=False)
    else:
        return err_response('invalid request')