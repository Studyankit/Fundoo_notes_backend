from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    date_of_birth = models.DateField(null=True)
    email = models.EmailField(max_length=100, unique=True)
    location = models.CharField(max_length=100, null=True)
    is_verify = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email']
