import jwt
import logging
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings

from user.models import User


class JWTEncodeDecode:
    """
    Encoding and decoding of data using jwt
    """

    @staticmethod
    def encode_data(payload):
        payload.update({"exp": settings.JWT_EXPIRING_TIME})
        print(payload)
        token_encoded = jwt.encode(payload, settings.JWT_SECRET_KEY,
                                   algorithm="HS256")
        return token_encoded

    @staticmethod
    def decode_data(token):
        token_decode = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        return token_decode


# def verify_token(function):
#     def wrapper(self, request):
#         # request.headers.get('token')
#         token = request.META.get('HTTP_TOKEN')
#         if not token:
#             return Response({'message': 'Not Authorized'}, status=status.HTTP_400_BAD_REQUEST)
#             # Getting user id from token
#         user_id = User.objects.get('username')
#         return function(self, request, user_id)
#
#     return wrapper

def verify_token(function):
    def wrapper(self, request, *args, **kwargs):
        # print('=====', request.META.get('HTTP_AUTHORIZATION'))
        if 'HTTP_AUTHORIZATION' not in request.META:
            resp = JsonResponse(
                {'message': 'Token not provided in the header'})
            resp.status_code = 400
            logging.info('Token not provided in the header')
            return resp
        token = request.META.get("HTTP_AUTHORIZATION")
        _, jwt_token = token.split(' ')
        payload = JWTEncodeDecode.decode_data(token=jwt_token)
        user = User.objects.get(username=payload.get('username'))
        request.user = user

        return function(self, request, *args, **kwargs)

    return wrapper
