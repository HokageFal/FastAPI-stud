from fastapi import FastAPI
from database import init_db
from shop.products.views import router as products_router
from shop.category.views import router as category_router
from users.routes.user import router as users_router
app = FastAPI()

app.include_router(products_router, )
app.include_router(category_router, )
app.include_router(users_router, )

ALGORITHM = 'HS256'