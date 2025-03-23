from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from channels.services.channels import create_channel, post_to_channel
from channels.services.posts_services import new_post, all_post, get_post
from database import get_db

from channels.models import Channel
from channels.schemas.chanel import channels
from channels.schemas.post import post
from users.services.permissions import is_autorization


router = APIRouter(prefix="/channels", tags=["Channels"])


# Маршрут для создания канала
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_channel_route(
    channel: channels,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(is_autorization)
):
    return await create_channel(db, channel, user)

@router.post("/post_add/", status_code=status.HTTP_201_CREATED)
async def create_post_route(post: post, db: AsyncSession = Depends(get_db)):
    return await new_post(db=db, post=post)

@router.get("/posts")
async def get_posts(db: AsyncSession = Depends(get_db)):
    return await all_post(db=db)

@router.get("/post/{id}")
async def get_post_id(id: int, db: AsyncSession = Depends(get_db)):
    return await get_post(db=db, id=id)

@router.get("/{id}/posts")
async def get_posts_channel(id: int, db: AsyncSession = Depends(get_db)):
    return await post_to_channel(db=db, id=id)