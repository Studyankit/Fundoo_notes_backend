import json
import pika
from django.core.mail import send_mail
from django.urls import reverse

from user.utils import JWTEncodeDecode

from django.conf import settings


class RabitServer:

    @staticmethod
    def send_mail_pika(data):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()

            channel.queue_declare(queue='send_mail')

            token = JWTEncodeDecode.encode_data(payload={'id': data.get('id'), 'email': data.get('email')})
            url = settings.BASE_URL + reverse('token_string', kwargs={'token': token})
            channel.basic_publish(exchange='', routing_key='send_mail', body=json.dumps({'url': url, 'email': data.get('email')}))
            connection.close()
        except Exception as e:
            print(e)
