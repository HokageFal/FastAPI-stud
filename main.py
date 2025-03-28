from fastapi import FastAPI
from database import init_db
from users.routers.user import router as users_router
from channels.routers.channel import router as channels_router
app = FastAPI()

app.include_router(users_router, )
app.include_router(channels_router, )
ALGORITHM = 'HS256'