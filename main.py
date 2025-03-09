from fastapi import FastAPI, Depends
from database import engine, Base, init_db
import models
from pydantic import BaseModel
from database import SessionLocal  # Это твоя сессия
from sqlalchemy.orm import Session
from datetime import date
from models import Product
from products.views import router as products_router

def get_db():
    db = SessionLocal()  # Создаем объект сессии
    try:
        yield db  # Возвращаем объект сессии
    finally:
        db.close()  # Закрываем сессию после использования

app = FastAPI()
app.include_router(products_router, )
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# @app.get('/add/products')
# def add_products(Product: products):
#