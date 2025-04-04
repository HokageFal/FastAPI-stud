from fastapi_cache.decorator import cache
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from channels.schemas.comment import comments
from channels.services.channels_service import create_channel, subscribe, subs_channels, unsubscribe, subs_count
from channels.services.comments_service import add_comment, get_comments_post, delete_comment
from channels.services.likes_service import add_like, get_like
from channels.services.posts_service import new_post, all_post, get_post, post_to_channel, subs_posts
from database import get_db

from channels.schemas.chanel import channels
from channels.schemas.post import post
from users.services.permissions import is_autorization

router = APIRouter(prefix="/channels", tags=["Channels"])

@router.post("/add", status_code=status.HTTP_201_CREATED, response_description="Создание нового канала")
async def create_channel_route(
    channel: channels,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(is_autorization),
    # file: UploadFile = None
):
    return await create_channel(db, channel, user)

@router.post("/posts/add", status_code=status.HTTP_201_CREATED, response_description="Добавить новый пост")
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

@router.post("/add_comment/{post_id}")
async def post_comment(post_id: int,  comment: comments, db: AsyncSession = Depends(get_db), user: dict = Depends(is_autorization)):
    return await add_comment(db=db, user=user, post_id=post_id, comment=comment)

@router.get("/comments/{post_id}")
async def comments_for_post(post_id: int, db: AsyncSession = Depends(get_db)):
    return await get_comments_post(post_id=post_id, db=db)

@router.delete("/comments/delete/{id}")
async def comments_delete_post(id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(is_autorization)):
    return await delete_comment(id=id, db=db, user=user)

@router.post("/add_like/{post_id}")
async def post_like(post_id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(is_autorization)):
    return await add_like(post_id=post_id, db=db, user=user)

@router.get("/likes/{post_id}")
async def likes_post(post_id: int, db: AsyncSession = Depends(get_db)):
    return await get_like(db=db, post_id=post_id)

@router.get("/subs/{channel_id}")
@cache(expire=10)
async def subs_post(channel_id: int, db: AsyncSession = Depends(get_db)):
    return await subs_count(db=db, channel_id=channel_id)