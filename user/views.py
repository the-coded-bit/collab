from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
from .utils import generate_jwt_token, ensure_valid_jwt
from django.contrib.auth import authenticate, login
import json


# Create your views here.
# register user (create user and sets jwt)
def register_user(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        first_name = json_data['first_name']
        last_name = json_data['last_name']
        username = json_data['username']
        password = json_data['password']
        email = json_data['email']
        try:
            user = User.objects.create_user(
                    username, 
                    email, 
                    password, 
                    last_name = last_name, 
                    first_name = first_name)
            jwt_token = generate_jwt_token(user.id)
            response = JsonResponse({'name': username, 'id': user.id})
            response.set_signed_cookie('access-token', jwt_token, settings.SECRET_KEY, httponly = True)
            return response
        except Exception as error:
            print(error)
            res = JsonResponse({'error': error.args})
            res.status_code = 400
            return res
    else:
        print(request.COOKIES)
        return JsonResponse({'invalid' : True}) 
    
# login user
def login(request):
     if request.method == 'POST':
        json_data = json.loads(request.body)
        username = json_data['username']
        password = json_data['password']
        response = None

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User is authenticated
            jwt_token = generate_jwt_token(user.id)
            response = JsonResponse({'status': 'login successful', 'id' : user.id})
            response.set_signed_cookie('access-token', jwt_token, settings.SECRET_KEY, httponly = True)
            return response
            # Redirect to a success page or perform other actions
        else:
            # Authentication failed
            # Handle invalid credentials
            response = JsonResponse({'error': ['invalid credentials']})
            response.status_code = 401
            return response

# logout user
def logout(request):
    response = JsonResponse({'message': 'Logout successful'})
    response.delete_cookie('access-token')
    return response

# get all users
@ensure_valid_jwt
def get_users(request):
    users = User.objects.all().values('username', 'email', 'id')
    users_list = list(users)
    return JsonResponse(users_list, safe=False)

    


