from fastapi import FastAPI, Depends
from database import engine, Base, init_db
import models
from pydantic import BaseModel
from database import SessionLocal  # Это твоя сессия
from sqlalchemy.orm import Session
from datetime import date
from models import Product


def get_db():
    db = SessionLocal()  # Создаем объект сессии
    try:
        yield db  # Возвращаем объект сессии
    finally:
        db.close()  # Закрываем сессию после использования

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/products")
def read_users(db: Session = Depends(get_db)):
    return db.query(Product).all()

class products(BaseModel):
    id:int
    name:str
    description: str
    price: int

# @app.get('/add/products')
# def add_products(Product: products):
#