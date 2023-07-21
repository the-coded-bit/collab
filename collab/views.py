from django.http import JsonResponse
from django.middleware.csrf import get_token

def home(request):
    csrf_token = get_token(request)
    res = JsonResponse({'message': 'setup done successfully'})
    # res.set_cookie('csrftoken', csrf_token)
    return res
