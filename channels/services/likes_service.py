from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from sqlalchemy import select, insert, func
from sqlalchemy.ext.asyncio import AsyncSession
from channels.models import Post
from channels.models import Likes


async def add_like(db: AsyncSession, post_id: int, user: dict):
    await db.execute(insert(Likes).values(post_id=post_id, user_id=user["id"]))
    await db.commit()

    return {"message": "Лайк добавлен"}

async def get_like(db: AsyncSession, post_id: int):
    likes_post = await db.scalar(select(func.count()).filter(Likes.post_id==post_id))
    return likes_post