from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from shop.category.schemas import categories
from shop.category.services import get_category, create_category, id_category, delete_category
from database import get_db

router = APIRouter(prefix="/category", tags=["Category"])

@router.get("")
def category_all(db: Session = Depends(get_db)):
    return get_category(db=db)

@router.post("/add")
def add_category(categories: categories, db: Session = Depends(get_db)):
    return create_category(db=db, category=categories)

@router.get("/{id}")
def category_id(id: int, db: Session = Depends(get_db)):
    return id_category(db=db, id=id)

@router.delete("/delete")
def category_delete(id: int, db: Session = Depends(get_db)):
    result = delete_category(db=db, id=id)
    return result

# @router.get("/products/{id}")
# def category_by_products(id:int, db: Session = Depends(get_db)):
#     return categories_products(db=db, id=id)