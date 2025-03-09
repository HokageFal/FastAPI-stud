from itertools import product

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, get_db

from models import Product
from products.services import create_product, get_products, id_products
from products.shemas import products

router = APIRouter(prefix="/products", tags=["products"])

@router.get("")
def read_products(db: Session = Depends(get_db)):
    return get_products(db=db)

@router.post("/add")
def create_new_product(product: products, db: Session = Depends(get_db)):
    return create_product(db=db, product=product)

@router.get("/{id}")
def product_id(id: int, db: Session = Depends(get_db)):
    return id_products(db=db, id=id)