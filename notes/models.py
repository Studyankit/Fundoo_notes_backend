from django.db import models
from user.models import User


# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    # note_id = models.IntegerField(primary_key=True, default=0)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)  # User = 'user.User'
