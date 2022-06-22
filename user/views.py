import jwt
import logging
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import status

from user.serializers import UserSerializer
from rest_framework.response import Response
from django.conf import settings
from user.models import User
from user.utils import JWTEncodeDecode
from user.utils import verify_token

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class UserAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="registration",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='first_name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='last_name'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
                'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='age'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='phone'),
            }
        ))
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

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="display",
    )
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

    @swagger_auto_schema(
        operation_summary="login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
            }
        ))
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
    @swagger_auto_schema(
        operation_summary="get user"
    )
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
