from django.urls import path

from user_content import views

urlpatterns = [
    path('login', views.UserLogin.as_view(), name='login'),
    path('register', views.UserRegistration.as_view(), name='register'),
    path('', views.index, name='index')
]
