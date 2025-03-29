from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
import redis.asyncio as redis
import time
from fastapi import FastAPI, UploadFile
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
import shutil
import os

UPLOAD_DIR = "media"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_media(file: UploadFile) -> str:
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path


# Данные для подключения
MYSQL_USER = "root"
MYSQL_PASSWORD = "9898"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "alembic_async"

# URL для асинхронного подключения
DATABASE_URL = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# Создаем асинхронный движок SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем асинхронную сессию
AsyncSessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

# Базовый класс для моделей
Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
ALGORITHM = 'HS256'

import redis

# Подключение к Redis
r = redis.Redis(
    host="localhost",
    port=6380,
    db=0,
    username="root",
    password=os.getenv("REDIS_PASSWORD"),
    # ssl=True,
    # ssl_cert_reqs=None
)
FastAPICache.init(RedisBackend(r), prefix="mycache")
# Проверка подключения
try:
    # Попытка выполнить команду PING
    response = r.ping()
    if response:
        print("Подключение к Redis успешно!")
    else:
        print("Не удалось подключиться к Redis.")
except Exception as e:
    print(f"Произошла ошибка: {e}")