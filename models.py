from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
import uuid

class Category(Base):
    __tablename__ = "Category"

    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    products = relationship("Product", back_populates="category")

class ProductSize(Base):
    __tablename__ = "ProductSize"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    length = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)

class Product(Base):
    __tablename__ = "Products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    price = Column(Integer)
    category_id = Column(Integer, ForeignKey("Category.id"))
    size_id = Column(Integer, ForeignKey("ProductSize.id"))
    size = relationship("ProductSize")
    category = relationship("Category", back_populates="products")