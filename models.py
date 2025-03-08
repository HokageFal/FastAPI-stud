from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
from datetime import datetime

class Product(Base):
    __tablename__ = "Products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    price = Column(Integer)
