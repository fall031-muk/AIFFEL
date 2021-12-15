import jwt

from django.http import JsonResponse

from config.settings import SECRET_KEY
from users.models import User

def signin_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.META.get('HTTP_AUTHORIZATION')
            payload = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')
            request.user = User.objects.get(id=payload['id'])

        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE':'INVALID_TOKEN'}, status=401)
            
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

        return func(self, request, *args, **kwargs)
    return wrapper