import json

from fastapi import FastAPI, WebSocket, Request, APIRouter
from typing import List, Dict
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from starlette.websockets import WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database import get_db
from users.models import Message
import redis.asyncio as redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from database import r
from fastapi.encoders import jsonable_encoder

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/message", tags=["message"])

class ConnectionManager:
    def __init__(self):
        self.connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.connections:
            del self.connections[user_id]

    async def send_message(self, recipient_id: int, message: str):
        if recipient_id in self.connections:
            await self.connections[recipient_id].send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{user_id}")
async def websocket_service(
    websocket: WebSocket,
    user_id: int,
    db: AsyncSession = Depends(get_db)
):

    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            recipient = data["recipient_id"]
            message_text = data["message"]

            await db.execute(insert(Message).values(
                sender_id=user_id,
                recipient_id=recipient,
                text=message_text
            ))
            await db.commit()

            await manager.send_message(recipient, message_text)
    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        await db.close()

@router.get("/websocket", response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/messages/{user_id}")
async def get_messages(user_id: int, db: AsyncSession = Depends(get_db)):
    cache_data = r.get(f"messages{user_id}")
    if cache_data:
        return json.loads(cache_data)

    result = await db.scalars(select(Message).filter((Message.sender_id == user_id) |
                                                     (Message.recipient_id == user_id)))
    messages = result.all()
    messages_json = jsonable_encoder(messages)
                                        #сек
    r.setex(f"messages:{user_id}", 300, json.dumps(messages_json))

    return messages_json