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
                if token:
                    try:
                        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                    except jwt.ExpiredSignatureError:
                        return err_response('JWT has expired')
                    except jwt.InvalidTokenError:
                        return err_response('Invalid JWT')
                    return view(request, *args, **kwargs )
            except Exception as err:
                print(err)
                return err_response('token does not exist')
    return wrapper
