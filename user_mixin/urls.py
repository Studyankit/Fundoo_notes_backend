from django.urls import path
from . import views

urlpatterns = [
    path('user_api/', views.UserMixin.as_view()),
    # path('user_api/<int:pk>/', views.UserCreate.as_view()),
    path('user_api/<int:pk>/', views.UserMixin.as_view())
]