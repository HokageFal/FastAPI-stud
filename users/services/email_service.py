import uuid
import os
from database import r
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from users.models import Users
from sqlalchemy import select
import smtplib

EMAIL = os.getenv("SENDER_EMAIL")
PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(email: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        # Настройка SMTP сервера
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Защищённое соединение
        server.login(EMAIL, PASSWORD)  # Логин в аккаунт
        server.sendmail(EMAIL, email, msg.as_string())  # Отправка письма
        server.quit()  # Завершаем сессию
        print(f"Email отправлен на {email}")
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")

def generate_activation_code():
    code = str(uuid.uuid4().int)[:6]  # Генерируем 6-значный код
    return code

def save_confirmation_code(email: str, code: str, expire_minutes: int = 10):
    r.setex(f"Код подтверждения:{email}", expire_minutes * 60, code)

def get_confirmation_code(email: str):
    code = r.get(f"Код подтверждения:{email}")
    return code.decode("utf-8") if code else None

async def code_send_email(email: str, db: AsyncSession, user: dict):
    user = await db.scalar(select(Users).filter(Users.id==user["id"]))

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if user.email is None or user.email == "":
        if not email:
            raise HTTPException(status_code=400, detail="Email не указан")

    if user.email is not None:
        email = user.email

    code = generate_activation_code()
    save_confirmation_code(email, code)

    subject = "Ваш код подтверждения"
    body = f"Здравствуйте!\n\nВаш код подтверждения: {code}\n\nС уважением, команда!"

    return send_email(email, subject, body)

async def verify_email(code: str, email: str, db: AsyncSession, user: dict):
    user = await db.scalar(select(Users).filter(Users.id==user["id"]))

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    verify_code = get_confirmation_code(email)

    if not verify_code:
        raise HTTPException(status_code=404, detail="Код не найден")

    if verify_code != code:
        raise HTTPException(status_code=400, detail="Код не верный")
    else:
        if user.email is None or user.email == "":
            user.email = email
        user.is_email_verified = True
        await db.commit()
    return {"message": "Вы успешно подтвердили свою почту"}
