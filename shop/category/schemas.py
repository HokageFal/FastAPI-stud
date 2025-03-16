from pydantic import BaseModel

class categories(BaseModel):
    name: str
    description: str