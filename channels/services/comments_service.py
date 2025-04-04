from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from channels.models import Comment, Post, Channel
from channels.schemas.comment import comments
from celery_app import comments_send_email

from users.models import Users


async def add_comment(db: AsyncSession, post_id: int, user: dict, comment: comments):
    post = await db.scalars(select(Post).filter(Post.id == post_id))
    post = post.first()
    channel = await db.scalars(select(Channel).filter(Channel.id == post.channel_id))
    channel = channel.first()
    owner = await db.scalars(select(Users).filter(Users.id==channel.owner_id))
    owner = owner.first()
    user_name = await db.scalars(select(Users).filter(Users.id == user["id"]))
    user_name = user_name.first()
    comments_send_email.delay(email=owner.email, user_name=user_name.name, post_name=post.title, comment=comment.comment)
    await db.execute(insert(Comment).values(comment=comment.comment, post_id=post_id, parent_id=comment.parent_id, user_id=user["id"]))
    await db.commit()

    return {"message": "Комментарий добавлен"}

async def get_comments_post(db: AsyncSession, post_id: int):
    result = await db.execute(select(Comment).filter(Comment.post_id==post_id))
    comments = result.scalars().all()

    if not comments:
        raise HTTPException(status_code=404, detail="Комментарии для данной публикации не найдены")

    comment_dict = {comment.id: comment for comment in comments}
    for comment in comments:
        comment.replies = []

    tree = []

    for comment in comments:
        if comment.parent_id:
            parent = comment_dict.get(comment.parent_id)
            if parent:
                parent.replies.append(comment)

        else:
            tree.append(comment)

    return tree

async def delete_comment(db: AsyncSession, id: int, user: dict):
    comment = await db.scalars(select(Comment).filter(Comment.id==id, Comment.user_id==user["id"]))
    comment = comment.first()

    if not comment:
        raise HTTPException(status_code=404, detail = "Комментарий не найден")

    await db.delete(comment)
    await db.commit()
    return {"message": "Комментарий успешно удален"}

