from rest_framework import serializers
from notes.models import User


class UserSerializer(serializers.ModelSerializer):
    """
        User Serializer
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'location', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id']

    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop('password')
        # ** validated_data = consecutive key = value pair
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
