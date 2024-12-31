"""
	Инициализация приложения Celery и фоновые задачи.
"""

from celery import Celery
import smtplib
from email.message import EmailMessage

from src.project import settings

celery = Celery("bg_tasker", broker=settings.REDIS_URL)


@celery.task
def send_message(
    email: EmailMessage,
) -> None:
    """
    Отправка email-сообщения в фоне через celery.
    :param email: email в формате EmailMessage.
    """
    with smtplib.SMTP_SSL(settings.EMAIL_SMTP_HOST, settings.EMAIL_SMTP_PORT) as server:
        server.login(settings.EMAIL_SMTP_USER, settings.EMAIL_SMTP_PWD)
        server.send_message(email)
