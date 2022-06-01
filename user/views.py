from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework import serializers, status
from user.serializers import UserSerializer
from rest_framework.response import Response

from user.models import User


class UserAPIView(APIView):

    def post(self, request):
        """
        Registration of new user by custom user model
        :param request: Add new user using POST
        :return: Json response with status code
        """
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        User Check if present or logged in
        :param request: Add new user using GET
        :return: Json response with status code
        """
        try:
            user = User.objects.get(username=request.data.get("username"))
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)


class LoginAPIView(APIView):

    def post(self, request):
        try:
            user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
            if user is not None:
                serializer = UserSerializer(user)
                return Response({'message': 'Login Successfully', 'data': serializer.data})
            else:
                return Response({'message': 'user not registered'}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
