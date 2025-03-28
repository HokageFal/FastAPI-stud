# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from database import get_db
#
# from shop.products.services import create_product, get_products, id_products, delete_product, product_by_category, \
#     update_products
# from shop.products.shemas import products
#
# router = APIRouter(prefix="/products", tags=["products"])
#
# @router.get("")
# def read_products(db: Session = Depends(get_db)):
#     return get_products(db=db)
#
# @router.post("/add")
# def create_new_product(product: products, db: Session = Depends(get_db)):
#     return create_product(db=db, product=product)
#
# @router.get("/{id}")
# def product_id(id: int, db: Session = Depends(get_db)):
#     return id_products(db=db, id=id)
#
# @router.delete("/delete")
# def product_delete(id: int, db: Session = Depends(get_db)):
#     return delete_product(db=db, id=id)
#
# @router.get("/category/{id}")
# def product_category_id(id: int, db: Session = Depends(get_db)):
#     return product_by_category(db=db,  id=id)
#
# @router.delete("/update/{id}")
# def up_products(product: products, id: int, db: Session = Depends(get_db)):
#     return update_products(db=db, id=id, product=product)
