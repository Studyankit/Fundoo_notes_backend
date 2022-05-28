import json

from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import serializers
from user.serializers import UserSerializer
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
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse({
                'message': 'User added successfully',
                'response': 200
            })
        except Exception as e:
            return JsonResponse({
                'message': 'User , enter proper registration details',
                'response': 404,
            })

    def get(self, request):
        """
        User Check if present or logged in
        :param request: Add new user using GET
        :return: Json response with status code
        """
        try:
            user = User.objects.get(username=request.data.get("username"))
            serializer = UserSerializer(user, many=True)
            return JsonResponse({
                'message': 'User already exists',
                'response': 200,
                'data': user.username
            })
        except Exception:
            return JsonResponse({
                'message': 'user needs to be added',
                'response': 404,
            })
