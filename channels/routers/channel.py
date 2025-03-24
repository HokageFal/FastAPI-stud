

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from channels.services.channels_service import create_channel, subscribe, subs_channels, unsubscribe
from channels.services.posts_service import new_post, all_post, get_post, post_to_channel, subs_posts
from database import get_db

from channels.models import Channel
from channels.schemas.chanel import channels
from channels.schemas.post import post
from users.services.permissions import is_autorization


router = APIRouter(prefix="/channels", tags=["Channels"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_description="Создание нового канала")
async def create_channel_route(
    channel: channels,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(is_autorization)
):
    return await create_channel(db, channel, user)


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_description="Добавить новый пост")
async def create_post_route(post: post, db: AsyncSession = Depends(get_db)):
    return await new_post(db=db, post=post)


@router.get("/posts", response_description="Все публикации")
async def get_posts(db: AsyncSession = Depends(get_db)):
    return await all_post(db=db)


@router.get("/posts/{id}", response_description="Получить публикацию по ID", response_model=post)
async def get_post_id(id: int, db: AsyncSession = Depends(get_db)):
    return await get_post(db=db, id=id)


@router.get("/{id}/posts", response_description="Все публикации канала")
async def get_posts_channel(id: int, db: AsyncSession = Depends(get_db)):
    return await post_to_channel(db=db, id=id)


@router.post("/{channel_id}/subscribe", status_code=status.HTTP_201_CREATED, response_description="Подписка на канал")
async def subscribe_to_channel(channel_id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(is_autorization)):
    return await subscribe(db, channel_id, user)

@router.delete("/{channel_id}/unsubscribe", status_code=status.HTTP_204_NO_CONTENT)
async def unsubscribe_to_channel(channel_id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(is_autorization)):
    return await unsubscribe(db, channel_id, user)

@router.get("/subs_posts", response_description="Публикации на каналах, на которые подписан пользователь")
async def subscribe_posts(db: AsyncSession = Depends(get_db), user: dict = Depends(is_autorization)):
    return await subs_posts(db=db, user=user)


@router.get("/subs_channels", response_description="Подписки пользователя на каналы")
async def subscribe_channels(db: AsyncSession = Depends(get_db), user: dict = Depends(is_autorization)):
    return await subs_channels(db=db, user=user)
