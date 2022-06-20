from celery import shared_task
from celery.utils.log import get_task_logger

from .email import send_mail, Email

logger = get_task_logger(__name__)


@shared_task
def send_email_task(email, subject, message):
    try:
        Email.send_email(email, subject, message)
    except Exception as e:
        print("task fail")
        logger.error(e)