from django.urls import path, include
from . import views

urlpatterns = [
    path('user/save/', views.user_registration, name='registration'),
    path('login/', views.user_login, name='login')
]