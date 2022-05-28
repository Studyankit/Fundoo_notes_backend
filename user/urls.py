from django.urls import path
from . import views

urlpatterns = [
    path('user/login/', views.UserModel.as_view()),
]