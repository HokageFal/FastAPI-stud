from typing import Optional

from pydantic import BaseModel

class comments(BaseModel):
    comment: str
    parent_id: Optional[int] = None