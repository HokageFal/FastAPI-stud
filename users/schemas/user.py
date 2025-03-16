from pydantic import BaseModel
from typing import Optional

class user(BaseModel):
    name: str
    surname: Optional[str] = None
    email: Optional[str] = None
    password: str