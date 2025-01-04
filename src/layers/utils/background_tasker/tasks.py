"""
	Инициализация приложения Celery и фоновые задачи.
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage

from celery import Celery

from src.project import settings

celery = Celery("bg_tasker", broker=settings.REDIS_URL)


# Создаем основной логгер для приложения
logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

# Создаем обработчик для вывода сообщений в консоль
fh = logging.FileHandler(".\\..\\..\\..\\..\\logs\\celery.log")
fh.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


@celery.task
def send_message(
    msg_subject: str,
    msg_text: str,
    send_to: str,
) -> None:
    """
    Отправка email-сообщения в фоне через celery.
    :param msg_subject: Тема письма
    :param msg_text: Текст письма
    :param send_to: Email-адрес получателя
    """

    with smtplib.SMTP_SSL(settings.EMAIL_SMTP_HOST, settings.EMAIL_SMTP_PORT) as server:

        server.login(user=settings.EMAIL_SMTP_USER, password=settings.EMAIL_SMTP_PWD)

        sender = settings.EMAIL_SMTP_USER

        email = create_email_message(
            msg_subject=msg_subject,
            msg_text=msg_text,
            send_from=sender,
            send_to=send_to,
        )

        server.sendmail(sender, send_to, email.as_string())


def create_email_message(
    msg_subject: str,
    msg_text: str,
    send_from: str,
    send_to: str,
) -> MIMEText:
    """Создание email сообщения для отправки через SMTP."""
    email = MIMEText(msg_text, "plain", "utf-8")
    email["Subject"] = msg_subject
    email["From"] = send_from
    email["To"] = send_to

    return email
