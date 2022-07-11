from django.db import models
from user.models import User


# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    collaborator = models.ManyToManyField(User, related_name='collaborator')


class Label(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    note = models.ManyToManyField(Note)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
