from models import Product
from products.shemas import products
from sqlalchemy.orm import Session
from sqlalchemy import select

def create_product(db: Session, product:  products):
    db_product = Product(name=product.name, description=product.description, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session) -> list[Product]:
    return db.query(Product).all()

def id_products(db: Session, id: int):
    return db.query(Product).filter(Product.id == id).first()