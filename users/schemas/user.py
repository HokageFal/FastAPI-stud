from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class user(BaseModel):
    name: str
    surname: str
    email: Optional[EmailStr] = None
    password: str
    register_data: Optional[datetime] = None  # Теперь не обязательно передавать
    is_admin: Optional[bool] = False  # По умолчанию False

class user_response(BaseModel):
    name: str
    surname: str
    email: str
    register_data: datetime
    is_admin: bool

    class Config:
        from_attributes = True

class Email(BaseModel):
    email: EmailStr
    code: Optional[str] = None
