from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from channels.models import Comment
from channels.schemas.chanel import channels
from channels.schemas.comment import comments


async def add_comment(db: AsyncSession, post_id: int, user: dict, comment: comments):
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