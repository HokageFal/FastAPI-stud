from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Данные для подключения (замени на свои)
MYSQL_USER = "root"
MYSQL_PASSWORD = "9898"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "cs"

# URL подключения к MySQL
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# Создаем движок SQLAlchemy
engine = create_engine(DATABASE_URL)

# Создаем сессию для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс моделей
Base = declarative_base()

def init_db():
    Base.metadata. create_all(bind=engine)

def get_db():
    db = SessionLocal()  # Создаем объект сессии
    try:
        yield db  # Возвращаем объект сессии
    finally:
        db.close()  # Закрываем сессию после использования
