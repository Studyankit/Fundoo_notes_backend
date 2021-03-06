from django.urls import path
from . import views

urlpatterns = [
    path('user/login/', views.LoginAPIView.as_view(), name='login'),
    path('user/', views.UserAPIView.as_view(), name='registration'),
    path('verify/<str:token>', views.ValidateToken.as_view(), name='token_string')
]