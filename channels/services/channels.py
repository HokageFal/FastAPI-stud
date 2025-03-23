from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from channels.models import Channel
from channels.schemas.chanel import channels
from users.services.permissions import is_autorization


async def create_channel(db: AsyncSession, channel: channels, user: dict = Depends(is_autorization)):
    await db.execute(insert(Channel).values(name=channel.name, description=channel.description, owner_id=user["id"]))
    await db.commit()

    return {"message": "Успешно создан канал"}

async def post_to_channel(db: AsyncSession, id: int):
    result = await db.execute(select(Channel).filter(Channel.id == id))  # используем execute вместо scalar
    channel = result.scalar_one_or_none()  # Получаем один объект или None

    if channel is None:
        return None

    return channel.posts
