import json, re
import bcrypt, jwt
import datetime

from django.http import JsonResponse
from django.views import View

from users.models import User
from config.settings import SECRET_KEY

class SignupView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            user_id  = data['user_id']
            password = data['password']
            
            if not (user_id and password):
                return JsonResponse({"MESSAGE":"EMPTY_VALUE_ERROR"}, status=400)
            
            if User.objects.filter(user_id=user_id).exists():
                return JsonResponse({"MESSAGE":"DUPLICATION_ERROR"}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_password = hashed_password.decode('utf-8')
            
            User.objects.create(
                user_id  = user_id,
                password = decoded_hashed_password,
            )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

class SigninView(View):   
    def post(self, request):
        try:
            data     = json.loads(request.body)
            user_id  = data['user_id']
            password = data['password']

            if not (user_id and password):
                return JsonResponse({"MESSAGE":"EMPTY_VALUE_ERROR"}, status=400)

            if not User.objects.filter(user_id=user_id).exists():
                return JsonResponse({"MESSAGE":"DOES_NOT_EXIST"}, status=401)

            user = User.objects.get(user_id=user_id)
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"MESSAGE":"INVALID_PASSWORD"}, status=401)
            
            access_token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm='HS256')
            return JsonResponse({"MESSAGE":"SUCCESS","ACCESS_TOKEN":access_token}, status=201)
                
        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status=400)