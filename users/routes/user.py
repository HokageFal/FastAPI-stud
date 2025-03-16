from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from users.schemas.user import user
from users.services.user_service import create_user, login
from typing import List, Any

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/add")
async def user_create(users: user, db: AsyncSession = Depends(get_db)) -> Any:
        return await create_user(db=db, users=users)

@router.post("/test")
async def user_get(users: user, response: Response, db: AsyncSession = Depends(get_db)):
        return await login(db=db, name=users.name, password=users.password, response=response)