import json
import logging

from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from rest_framework.views import APIView

from user.models import User
from user.serializers import UserSerializer


def index(request):
    return render(request, "index.html")


class UserRegistration(APIView):

    def post(self, request):

        try:
            data = User.objects.create_user(username=request.data.get('username'),
                                            password=request.data.get('password'))
            print(data)
            return render(request, 'register.html', {'data': request.data})
        except Exception as e:
            logging.error(e)
            return render(request, 'register.html')

    def get(self, request):
        return render(request, 'register.html')


class UserLogin(APIView):

    def post(self, request):

        try:
            user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
            if user is not None:
                serializer = UserSerializer(user)
                return render(request, 'login.html', {'message': 'Login Successfully', "data": serializer.data})
            else:
                return render(request, 'login.html', {'message': 'Login Unsuccessfull'})

        except Exception as e:
            return render(request, "login.html", {'message': str(e)})

    def get(self, request):
        return render(request, 'login.html')
