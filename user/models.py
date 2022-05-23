from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class User(AbstractUser):
    date_of_birth = models.DateField()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
