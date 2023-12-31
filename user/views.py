from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
from .utils import generate_jwt_token, ensure_valid_jwt, err_response
from django.contrib.auth import authenticate
import json
import jwt


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
            response = JsonResponse({'name': username, 'id': user.id, 'username': username, 'email': email})
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
        try:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # User is authenticated
                jwt_token = generate_jwt_token(user.id)
                response = JsonResponse({'status': 'login successful', 'id' : user.id, 'username': user.get_username()})
                response.set_signed_cookie('access-token', jwt_token, settings.SECRET_KEY, httponly = True)
                return response
                # Redirect to a success page or perform other actions
            else:
                # Authentication failed
                # Handle invalid credentials
                response = JsonResponse({'error': ['invalid credentials']})
                response.status_code = 401
                return response
        except:
            return err_response('Invalid credentials')

# logout user
def logout(request):
    response = JsonResponse({'message': 'Logout successful'})
    response.delete_cookie('access-token')
    return response

# get all users
@ensure_valid_jwt
def get_users(request):
    users = User.objects.all()
    user_list = [
        {
            'username': user.username,
            'email': user.email,
            'id': str(user.id),  # Convert 'id' to a string
        }
        for user in users
    ]

    return JsonResponse(user_list, safe=False)

#get users by id
@ensure_valid_jwt
def get_user_by_id(request):
    if request.method == 'GET':
         token = request.get_signed_cookie('access-token', salt = settings.SECRET_KEY)
         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
         user = User.objects.get(id = payload['id'])
         
         return JsonResponse({'id': user.id, 'username': user.username, 'email': user.email}, safe=False)
    else:
        return err_response('invalid request')


    


