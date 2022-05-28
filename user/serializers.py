from rest_framework import serializers
from notes.models import User


class UserSerializer(serializers.ModelSerializer):
    """
        User Serializer
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'username', 'location', 'password']
