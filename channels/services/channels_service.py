from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from sqlalchemy import select, insert, func
from sqlalchemy.ext.asyncio import AsyncSession

from channels.models import Channel, Post, Subscription
from channels.schemas.chanel import channels
from channels.schemas.subscribe import subsribes
from users.services.permissions import is_autorization

async def create_channel(db: AsyncSession, channel: channels, user: dict):
    await db.execute(insert(Channel).values(name=channel.name, description=channel.description, owner_id=user["id"]))
    await db.commit()

    return {"message": "Успешно создан канал"}

async def subscribe(db: AsyncSession, channel_id: int, user: dict):
    channel = await db.execute(select(Channel).filter(Channel.id == channel_id))
    if not channel.scalars().first():
        raise HTTPException(status_code=404, detail="Канал не найден")

    existing = await db.execute(select(Subscription).filter_by(user_id=user["id"], channel_id=channel_id))
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="Вы уже подписаны")

    await db.execute(insert(Subscription).values(channel_id=channel_id, user_id=user["id"]))
    await db.commit()

    return {"message": "Вы подписались на канал"}

async def unsubscribe(db: AsyncSession, channel_id: int, user: dict):
    channel = await db.execute(select(Channel).filter(Channel.id == channel_id))
    if not channel.scalars().first():
        raise HTTPException(status_code=404, detail="Канал не найден")

    existing = await db.execute(select(Subscription).filter_by(user_id=user["id"], channel_id=channel_id))
    existing = existing.scalars().first()

    if existing:
        await db.delete(existing)
        await db.commit()
        return {"message": "Вы успешно отписались от этого канала"}
    else:
        raise HTTPException(status_code=400, detail="Вы не подписаны на этот канал")

async def subs_channels(db: AsyncSession, user: dict):
    channels_id = await db.execute(select(Subscription.channel_id).filter(Subscription.user_id==user["id"]))
    channels_id = channels_id.scalars().all()

    if not channels_id:
        raise HTTPException(status_code=404, detail="Нет подписок на каналы")

    channels = await db.execute(select(Channel).filter(Channel.id.in_(channels_id)))
    channels = channels.scalars().all()

    if not channels:
        raise HTTPException(status_code=404, detail="Нет каналов, на которые вы подписаны")

    return channels

async def subs_count(db: AsyncSession, channel_id: int):
    result = await db.scalar(select(func.count()).filter(Subscription.channel_id==channel_id))
    return result