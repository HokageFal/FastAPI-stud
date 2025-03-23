from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from users.schemas.user import user
from users.services.user_service import create_user, user_login, update_access, user_view, user_logout
from typing import List, Any

router = APIRouter(prefix="/users", tags=["User"])

@router.post("/add")
async def user_create(users: user, db: AsyncSession = Depends(get_db)) -> Any:
        return await create_user(db=db, users=users)

@router.post("/login")
async def login(users: user, response: Response, db: AsyncSession = Depends(get_db)):
        return await user_login(db=db, name=users.name, password=users.password, response=response)

@router.post("/access")
async def access_token(request: Request, db: AsyncSession = Depends(get_db)):
        return await update_access(db=db, request=request)

@router.get("/view")
async def user_get(request: Request, db: AsyncSession = Depends(get_db)):
        return await user_view(db=db, request=request)

@router.post("/logout")
async def logout(response: Response):
        return await user_logout(response=response)
