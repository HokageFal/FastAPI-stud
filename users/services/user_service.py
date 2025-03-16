from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy import select, insert
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from database import SECRET_KEY, ALGORITHM
from users.schemas.user import user
from users.models import Users
from datetime import datetime, timedelta
import jwt

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(db: AsyncSession, users: user):
    await db.execute(insert(Users).values(name=users.name, surname=users.surname,
                                         email=users.email, password=bcrypt_context.hash(users.password)))

    await db.commit()
    return  {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Ok"
    }

async def login(db: AsyncSession, name: str, password: str, response: Response):
    result = await db.scalars(select(Users).filter(Users.name == name))
    user = result.first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')

    if not bcrypt_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Неверный пароль")

    access_payload = {
        "id": user.id,
        "type": "access",
        "is_admin": user.is_admin,
        "iat": datetime.utcnow() + timedelta(minutes=59),
        "exp": datetime.utcnow()
    }
    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)

    refresh_payload = {
        "id": user.id,
        "type": "refresh",
        "is_admin": user.is_admin,
        "iat": datetime.utcnow() + timedelta(days=15),
        "exp": datetime.utcnow()
    }
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)

    response.set_cookie(key="jwt", value=refresh_token, httponly=True, samesite="None")

    return {"access_token": access_token,
            "refresh_token": refresh_token}

