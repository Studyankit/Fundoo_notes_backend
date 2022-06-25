import jwt
import logging
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status

from user.serializers import UserSerializer
from rest_framework.response import Response
from django.conf import settings
from user.models import User
from user.utils import JWTEncodeDecode
from user.utils import verify_token


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
            user = User.objects.get(username=serializer.validated_data.get('username'))
            mail_subject = "Verification mail"
            token = JWTEncodeDecode.encode_data(payload={'id': user.id, 'username': user.username})
            mail_message = "Click on this http://127.0.0.1:8000/verify/" + token
            print(mail_message)
            send_mail(mail_subject, mail_message, settings.FROM_EMAIL,
                      [user.email], fail_silently=False)
            print(serializer.validated_data)
            return render(request, 'login')
            # return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def get(self, request):
        """
        User Check if present or logged in
        :param request: Add new user using GET
        :return: Json response with status code
        """
        try:
            print(request.data)
            # user = User.objects.get(username=request.data.get('username'))
            user = User.objects.get(id=request.data.get('user'))
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)


class LoginAPIView(APIView):
    """
    Logged user check method to see if user is in database
    """

    def post(self, request):
        try:
            user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
            if user is not None:
                token = JWTEncodeDecode.encode_data(payload={'id': user.id, 'username': user.username})
                payload = {'token': token}
                return Response({'message': 'Login Successfully', 'data': payload})
            else:
                return Response({'message': 'user not registered'}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ValidateToken(APIView):
    """
    Validating the token if the user is valid or not
    """

    def get(self, request, token):

        try:
            decode_token = JWTEncodeDecode.decode_data(token=token)
            user = User.objects.get(username=decode_token.get('username'))
            user.is_verify = True
            user.save()
            return Response({"message": "Validation Successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            logging.error(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
