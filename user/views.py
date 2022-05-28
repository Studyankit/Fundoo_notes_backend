import json

from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from user.models import User


class UserModel(APIView):

    def post(self, request):
        """
        Registration of new user by custom user model
        :param request: Add new user using POST
        :return: Json response with status code
        """
        try:
            data = json.loads(request.body)
            register_user = User.objects.create_user(username=data.get("username"), email=data.get("email"))
            authorize_user = authenticate(username=data.get('username'), email=data.get('email'))
            return JsonResponse({
                'message': 'User added successfully',
                'response': 200
            })
        except Exception as e:
            return JsonResponse({
                'message': 'User not there or enter proper registration details',
                'response': 404,
            })

    def get(self, request):
        """
        User Check if present or logged in
        :param request: Add new user using GET
        :return: Json response with status code
        """
        try:
            data = json.loads(request.body)
            user_check_login = User.objects.filter(username=data.get("username"), email=data.get("email"))
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
