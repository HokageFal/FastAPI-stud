from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from channels.models import Channel, Post
from channels.schemas.chanel import channels
from channels.schemas.post import post
from users.services.permissions import is_autorization

async def new_post(db: AsyncSession, post: post):
    await db.execute(insert(Post).values(title=post.title, description=post.description,
                                         channel_id=post.channel_id, media_url=post.media_url))
    await db.commit()

    return {"message": "Публикация была добавлена"}

async def all_post(db: AsyncSession):
    result = await db.scalars(select(Post))
    return result.all()

async def get_post(db: AsyncSession, id: int):
    result = await db.scalars(select(Post).filter(Post.id==id))
    return result.first()
