from fastapi import status, HTTPException, Response, Request, UploadFile
from sqlalchemy import select, insert
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from database import SECRET_KEY, ALGORITHM, save_media
from users.schemas.user import user, user_response
from users.models import Users
from datetime import datetime, timedelta
import jwt

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(db: AsyncSession, users: user, file: UploadFile = None):

    result = await db.scalars(select(Users).filter(Users.email == users.email))
    existing_user = result.first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Пользователь с таким email уже существует")

    media_url = None
    if file:
        media_url = await save_media(file)

    await db.execute(insert(Users).values(
        name=users.name,
        surname=users.surname,
        email=users.email,
        password=bcrypt_context.hash(users.password),
        avatar=media_url
    ))

    await db.commit()

    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Ok"
    }

async def user_login(db: AsyncSession, name: str, password: str, response: Response):
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
        "iat": datetime.utcnow(),  # ✅ Указываем текущее время
        "exp": datetime.utcnow() + timedelta(minutes=59)  # ✅ Истекает через 59 минут
    }
    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)

    refresh_payload = {
        "id": user.id,
        "type": "refresh",
        "is_admin": user.is_admin,
        "iat": datetime.utcnow(),  # ✅ Указываем текущее время
        "exp": datetime.utcnow() + timedelta(days=15)  # ✅ Истекает через 59 минут
    }
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)

    response.set_cookie(key="jwt", value=refresh_token, httponly=True, samesite="None")

    return {"access_token": access_token,
            "refresh_token": refresh_token}

async def update_access(request: Request):
    data = await request.json()
    refresh = data.get("refresh_token")


    if not refresh:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='токен не найден')

    refresh_payload = jwt.decode(refresh, SECRET_KEY, algorithms=[ALGORITHM])

    access_payload = {
        "id": refresh_payload["id"],
        "type": "access",
        "is_admin": refresh_payload["is_admin"],
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=59),

    }

    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token
    }

async def user_view(db: AsyncSession, request: Request):
    access = request.headers.get("Authorization")

    if not access:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='токен не найден')

    if access.split()[0] != "Bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный формат токена")

    token = access.split()[1]

    decode_access = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    user = await db.scalars(select(Users).filter(Users.id == decode_access["id"]))
    result = user.first()
    return user_response.model_validate(result)

async def user_logout(response: Response):
    response.delete_cookie(key="jwt")
    return {"message": "Вы успешно вышли из аккаунта"}