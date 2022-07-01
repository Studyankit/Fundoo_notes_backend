import json
import pika, sys, os
from django.core.mail import send_mail
from django.conf import settings


class RabitReceive:

    @staticmethod
    def send_mail_receive(body):
        try:
            data = json.loads(body)
            mail_subject = "Verification mail"
            mail_message = "Click on this " + data.get('url')
            send_mail(mail_subject, mail_message, settings.FROM_EMAIL, [data.get('email')], fail_silently=False)
            return True
        except Exception as e:
            print(e)

    @staticmethod
    def receive_mail_pika():
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='send_mail')

        def callback(body):
            RabitReceive.send_mail_receive(body)
            print(" [x] Received %r" % body)

        channel.basic_consume(queue='send_mail', on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

# if __name__ == '__main__':
#     try:
#         RabitReceive.receive_mail_pika()
#     except KeyboardInterrupt:
#         print('Interrupted')
#         try:
#             sys.exit(0)
#         except SystemExit:
#             os._exit(0)
