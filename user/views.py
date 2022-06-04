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
from user.jwtauthenticate import JWTEncodeDecode


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
            user = User.objects.get(username=request.data.get('username'))
            mail_subject = "Verification mail"

            token = jwt.encode({"id": user.id, 'username': user.username},
                               settings.JWT_SECRET_KEY, algorithm="HS256")
            mail_message = "Click on this http://127.0.0.1:8000/verify/" + JWTEncodeDecode.encode_data(payload=user.id)
            print(mail_message)
            send_mail(mail_subject, mail_message, settings.FROM_EMAIL, [request.data.get('email')], fail_silently=False)
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
    """
    Logged user check method to see if user is in database
    """

    def post(self, request, token):
        try:
            user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
            if user is not None:
                encoded_token = jwt.encode({"id": user.id, 'username': user.username}, settings.JWT_SECRET_KEY,
                                           algorithm="HS256")
                # token = JWTEncodeDecode.encode_data(payload=user.id)
                serializer = UserSerializer(user)
                return Response({'message': 'Login Successfully', 'data': serializer.data})
            else:
                return Response({'message': 'user not registered'}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ValidateToken(APIView):

    def get(self, request, token):

        try:
            decode_token = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
            print(decode_token)
            user = User.objects.get(username=decode_token.get('username'))
            user.is_verify = True
            user.save()
            return Response({"message": "Validation Successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            logging.error(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
