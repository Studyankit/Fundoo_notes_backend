from django.urls import path
from . import views

urlpatterns = [
    path('user/save/', views.user_registration, name='registration'),
    path('user/login/', views.user_login, name='login'),
    path('user/authenticate/', views.user_authenticate, name='authenticate')
]