import json

from django.http import JsonResponse
from django.contrib.auth import authenticate

# Create your views here.
from user.models import User


def user_registration(request):
    """
    Registration of new user by custom user model
    :param request: Add new user using POST
    :return: Json response with status code
    """
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            register_user = User.objects.create(username=data.get("username"), email=data.get("email"))
            return JsonResponse({
                'message': 'User added successfully',
                'response': 200
            })
    except Exception as e:
        return JsonResponse({
            'message': 'User not there or enter proper registration details',
            'response': 404,
        })


def user_login(request):
    """
    User Check if present or logged in
    :param request: Add new user using GET
    :return: Json response with status code
    """
    try:
        if request.method == "GET":
            data = json.loads(request.body)
            user_check_login = User.objects.get(username=data.get("username"), email=data.get("email"))
            return JsonResponse({
                'message': 'User already exists',
                'response': 200,
                'data': user_check_login.username
            })
    except Exception:
        return JsonResponse({
            'message': 'user needs to be added',
            'response': 404,
        })


def user_authenticate(request):
    """
    User validation for custom user model
    """
    try:
        if request.method == "GET":
            data = json.loads(request.body)
            authorize_user = authenticate(username=data.get('username'), email=data.get('email'))
            if authorize_user is not None:
                return JsonResponse({
                    'message': 'User validation successfully',
                    'response': 200,
                })
            else:
                return JsonResponse({
                    'message': 'User validation failed',
                    'response': 400,
                })
    except Exception:
        return JsonResponse({
            'message': 'user needs to be added',
            'response': 404,
        })