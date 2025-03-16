from pydantic import BaseModel

class sizes(BaseModel):
    title: str
    length: int
    width: int
    height: int

class products(BaseModel):
    id: int
    name:str
    description: str
    price: int
    category_id: int
    size_id: int
    size: sizes
