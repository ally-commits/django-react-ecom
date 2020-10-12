from rest_framework import viewsets
from rest_framework.permission import AllowAny
from .serializers import UserSerailizers
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logut

import random
import re

def generate_session_token(length=10):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97,123)] + [str(i) for i in range(10)]) for _ in range(length))

@csrf_exempt
def signin(request):
    if not request.method = "POST":
        return JsonResponse({'error': "Send a Post method with valid parameter"})

    username = request.POST['email']
    password = request.POST['password']

    if not re.match("^[\w\.\+\-]\@[\w]+\.[a-z]{2,3}$",username):
        return JsonResponse({'error': "Enter a Valid email"})

    if len(password) < 3:
        return JsonResponse({'error': "Password needs to be atleast 3 char"})

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(email=username)

        if(user.check_password(password)):
            user_dict = UserModel.objects.filter(email=username).values().first()
            user_dict.pop('password')

            if user.session_token != "0":
                user.session_token = "0"
                user.save()

                return JsonResponse({'error': "Previous session exists!"})
            
            token = generate_session_token()

            user.session_token = token
            user.save()

            login(request,user)

            return JsonResponse({'token',token, 'user': user_dict})
        else:
            return JsonResponse({'error': 'Invalid Password '})

    except UserModel.DoesNotExist:
        return JsonResponse({"error": "Invalid Email"})

def signout(request,id):
    logout(request)

    UserModel = get_user_model()

    try:
        user = UserModel.objects(pk=id)
        user.session_token = "0"
        user.save()

    except UserModel.DoesNotExist:
        return JsonResponse({'error': "Invalid User Id"})

    return JsonResponse({'success': "Logout Success"})
    