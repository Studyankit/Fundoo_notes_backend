from django.urls import path, include
from . import views

urlpatterns = [
    path('registration/', views.user_registration, name='registration'),
    path('login/', views.user_login, name='login')
]