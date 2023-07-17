import jwt
from datetime import datetime, timedelta
from django.http import HttpResponseBadRequest, JsonResponse
from django.conf import settings
import json

# create jwt token
def generate_jwt_token(id):
    jwt_token = jwt.encode(
        {
        'id': id, 
        'exp': datetime.utcnow() + timedelta(days= 1)
        }, settings.SECRET_KEY, algorithm='HS256')
    return jwt_token

# get json response for error messages
def err_response(message):
    return JsonResponse({'error': message}, status=400)

# validate jwt token
# protect routes with this given validation
def ensure_valid_jwt(view):
    def wrapper(request ,*args, **kwargs):
            try:
                token = request.get_signed_cookie('access-token', salt = settings.SECRET_KEY)
                user_id = request.GET['id']
                print('user id', user_id)
                if token:
                    try:
                        # print(args[0])
                        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                        # print(payload['id'], payload['id'] == int(user_id))
                        if payload['id'] != int(user_id):
                            return err_response('invalid user')
                    except jwt.ExpiredSignatureError:
                        return err_response('JWT has expired')
                    except jwt.InvalidTokenError:
                        return err_response('Invalid JWT')
                    return view(request, *args, **kwargs )
            except Exception as err:
                return err_response('token does not exist')
    return wrapper
