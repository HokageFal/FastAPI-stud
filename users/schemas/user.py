from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class user(BaseModel):
    name: str
    surname: Optional[str] = None
    email: Optional[str] = None
    password: str

class user_response(BaseModel):
    name: str
    surname: str
    email: str
    register_data: datetime
    is_admin: bool

    class Config:
        from_attributes = True