from django.conf import settings
from django.core.mail import send_mail


class Email:

    @staticmethod
    def send_email(email, subject, message, data={}):
        mail = send_mail(subject, message, settings.FROM_EMAIL,
                         [email], fail_silently=False)
        return mail
