from pydantic import BaseModel

class post(BaseModel):
    channel_id: int
    title: str
    description: str
    media_url: str
