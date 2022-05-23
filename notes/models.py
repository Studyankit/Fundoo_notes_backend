from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class UserProfile(models.Model):
    user_name = models.CharField(max_length=50, unique=True) # make it unique field
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100, null=True)
    phone_no = models.BigIntegerField(null=True)
    location = models.CharField(max_length=100, null=True)

