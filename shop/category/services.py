from models import Category
from shop.category.schemas import categories
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import select

# def get_category(db: Session) -> list[Category]:
#     return db.query(Category).all()

def get_category(db: Session) -> list[Category]:
    result = db.scalars(select(Category)).all()
    if result is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Категории с таким id не существует'
        )
    return result

# def create_category(db: Session, category: categories) -> list[Category]:
#     category_db = Category(name=category.name, description=category.description)
#     db.add(category_db)
#     db.commit()
#     db.refresh(category_db)
#     return category_db

# Новый синтаксис (SQLAlchemy 2.0)
def create_category(db: Session, category: categories) -> list[Category]:
    category_db = Category(name=category.name, description=category.description)
    db.execute(select(Category).where(Category.name == category.name))
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db

# Старый синтаксис (SQLAlchemy 1.x)
# def id_category(db: Session, id:int):
#     return db.query(Category).filter(Category.id == id).first()

# Новый синтаксис (SQLAlchemy 2.0)
def id_category(db: Session, id: int):
    result = db.scalars(select(Category).where(Category.id == id)).first()
    if result is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Категории с таким id не существует'
        )
    return result

# def delete_category(db: Session, id: int):
#     category = db.query(Category).filter(Category.id == id).first()

def delete_category(db: Session, id: int):
    result = db.scalars(select(Category).where(Category.id == id)).first()

    if result:
        db.delete(result)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Категории с таким id не существует")

# def categories_products(db: Session, id: int):
#     category = db.query(Category).filter(Category.id == id).first()
#     return category.products

# def categories_products(db: Session, id: int):
#     result = db.execute(select(Category).where(Category.id == id)) Такое уже есть в продуктах
#     category = result.scalars().first()
#     return category.products if category else None
