from fastapi import APIRouter, Depends, status, HTTPException, Response, Request, UploadFile
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from channels.models import Channel, Post, Subscription
from channels.schemas.chanel import channels
from channels.schemas.post import post
from database import save_media
from users.services.permissions import is_autorization
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from channels.models import Post, Subscription


async def new_post(db: AsyncSession, post: post):
    # media_url = None
    # if file:
    #     media_url = await save_media(file)

    await db.execute(insert(Post).values(
        title=post.title,
        description=post.description,
        channel_id=post.channel_id,
        # media_url=media_url,
    ))
    await db.commit()
    return {"message": "Публикация была добавлена"}

async def all_post(db: AsyncSession):
    result = await db.scalars(select(Post))
    posts = result.all()
    if not posts:
        raise HTTPException(status_code=404, detail="Публикации не найдены")
    return posts

async def get_post(db: AsyncSession, id: int):
    result = await db.scalars(select(Post).filter(Post.id == id))
    post = result.first()
    if not post:
        raise HTTPException(status_code=404, detail="Публикация не найдена")
    return post

async def post_to_channel(db: AsyncSession, id: int):
    result = await db.execute(select(Post).filter(Post.channel_id == id))
    posts = result.scalars().all()

    if not posts:  # Если постов нет для этого канала
        raise HTTPException(status_code=404, detail="Посты для данного канала не найдены")

    return posts

async def subs_posts(db: AsyncSession, user: dict):
    channels_id_result = await db.execute(select(Subscription.channel_id).filter(Subscription.user_id == user["id"]))
    channels_id = channels_id_result.scalars().all()

    if not channels_id:
        raise HTTPException(status_code=404, detail="Нет подписок на каналы")

    posts_result = await db.execute(select(Post).filter(Post.channel_id.in_(channels_id)))
    posts = posts_result.scalars().all()

    if not posts:
        raise HTTPException(status_code=404, detail="Нет постов для ваших подписанных каналов")

    return posts
