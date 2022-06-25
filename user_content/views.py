import json
import logging

from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.views import View

from user.models import User


def index(request):
    user = User.objects.get(id=2)
    return render(request, "index.html", {'message': "Home Page", 'mdata': 'Home redirect', 'user_object': user})


class UserRegistration(View):

    def post(self, request):

        try:
            User.objects.create_user(username=request.POST.get('username'),
                                     password=request.POST.get('password'), email=request.POST.get('email'),
                                     location=request.POST.get('location'))
            return redirect('login')
        except Exception as e:
            logging.error(e)
            return render(request, 'register.html', {'m': str(e)})

    def get(self, request):
        return render(request, 'register.html')


class UserLogin(View):

    def post(self, request):

        try:
            user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
            if user is not None:
                request.user = user
                return redirect('index')
            return render(request, 'login.html', {'message': 'Login Unsuccessfull'})

        except Exception as e:
            return render(request, "login.html", {'message': str(e)})

    def get(self, request):
        return render(request, 'login.html')
