import os
import time
from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://:9898@redis:6379/0")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://:9898@redis:6379/0")

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from users.services.email_service import EMAIL, PASSWORD, SMTP_SERVER, SMTP_PORT, send_email


@celery.task(name="channel_send_email")
def channel_send_email(email: str, channel_name: str):
    subject = "Создание канала"
    body = (f"Здравствуйте!\n\nПоздравляем вас с успешным "
            f"созданием нового канала: {channel_name}\n\nС уважением, команда!")

    return send_email(email, subject, body)

@celery.task(name="comments_send_email")
def comments_send_email(email: str, user_name: str, comment: str, post_name: str):
    subject = f"На вашу публикацию {post_name} был добавлен комментарий от пользователя {user_name}"
    body = (f"Здравствуйте!\n\nНа вашу публикаю был добавлен новый комментарий "
            f"{comment}\n\nС уважением, команда!")

    return send_email(email, subject, body)