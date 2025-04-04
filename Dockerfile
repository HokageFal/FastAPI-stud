# Используем Python 3.9
FROM python:3.9

# Устанавливаем рабочую директорию в корень проекта
WORKDIR /code

# Копируем зависимости
COPY ./requirements.txt /code/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Копируем весь проект (включая main.py, модели и т. д.)
COPY . /code

# Устанавливаем wait-for-it (ожидание БД)
RUN apt-get update && apt-get install -y wait-for-it

# Запускаем FastAPI из корня
CMD ["wait-for-it", "postgres:5432", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
