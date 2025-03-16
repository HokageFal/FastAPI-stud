from itertools import product

from models import Product, ProductSize, Category
from shop.products.shemas import products
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import insert, select, update

def create_product(db: Session, product: products):
    # Создание нового размера
    size_stmt = insert(ProductSize).values(
        title=product.size.title,
        length=product.size.length,
        width=product.size.width,
        height=product.size.height
    )

    # Выполнение запроса на вставку
    result = db.execute(size_stmt)
    db.commit()  # Подтверждаем изменения
    size_id = result.inserted_primary_key[0]  # Получаем id вставленного размера

    # Создание нового продукта
    product_stmt = insert(Product).values(
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id,
        size_id=size_id
    )

    # Выполнение запроса на вставку
    db.execute(product_stmt)
    db.commit()  # Подтверждаем изменения

    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

def get_products(db: Session) -> list[Product]:
    # return db.query(Product).all()
    return db.scalars(select(Product)).all()


def id_products(db: Session, id: int):
    # return db.query(Product).filter(Product.id == id).first()
    query = db.scalars(select(Product).filter(Product.id == id)).first()
    if query is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Продукта с таким id не существует'
        )
    return query

def delete_product(db: Session, id: int):
    # product = db.query(Product).filter(Product.id == id).first()
    product = db.scalars(select(Product).filter(Product.id == id)).first()

    if product:
        db.delete(product)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Продукт не найден")

def product_by_category(db: Session, id: int):
    # return db.query(Product).filter(Product.category_id == id).all()
    query = db.scalars(select(Product).filter(Product.category_id == id)).first()
    if query is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Категории с таким id не существует'
        )
    return query

def update_products(db: Session, id: int, product:  products):
    product_update = db.scalars(select(Product).filter(Product.id == id)).first()
    if product_update is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Продукта с таким id не существует'
        )
    db.execute(update(Product).filter(Product.id == id).values(name=product.name, description=product.description,
                                            price=product.price, category_id=product.category_id, size_id=product.size_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Product update is successful'
    }