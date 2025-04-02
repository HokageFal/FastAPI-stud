from celery_app import celery
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from users.services.email_service import EMAIL, PASSWORD, SMTP_SERVER, SMTP_PORT
@celery.task
def channel_send_email(email: str, channel_name: str):
    subject = "Создание канала"
    body = (f"Здравствуйте!\n\nПоздравляем вас с успешным "
            f"созданием нового канала: {channel_name}\n\nС уважением, команда!")

    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, email, msg.as_string())
        server.quit()
        return f"Email отправлен на {email}"  # ✅ Возвращает успех
    except Exception as e:
        return f"Ошибка при отправке письма: {e}"  # ✅ Возвращает ошибку
