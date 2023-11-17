"""
Main file
"""
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from auth.routes import auth_router
from api.wishlist_routes import api_router
from api.chat_routes import chat_router
from config import settings


import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise

from examples.constants import BASE_DIR
from models.admin import Admin
from examples.providers import LoginProvider
from fastapi_admin.app import app as admin_app
from fastapi_admin.exceptions import (
    forbidden_error_exception,
    not_found_error_exception,
    server_error_exception,
    unauthorized_error_exception,
)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def init():
    """
    Initial method
    """
    r = redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
        encoding="utf8",
    )
    await admin_app.configure(
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        template_folders=[os.path.join(BASE_DIR, "templates")],
        favicon_url="https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/favicon.png",
        providers=[
            LoginProvider(
                login_logo_url="https://preview.tabler.io/static/logo.svg",
                admin_model=Admin,
            )
        ],
        redis=r,
    )
    await Tortoise.init(
        db_url=settings.DATABASE_URL, modules={"models": settings.MODULE_LIST}
    )


@app.on_event("shutdown")
async def shutdown_db():
    """
    Shutdown method
    """
    await Tortoise.close_connections()


app.include_router(auth_router)
app.include_router(api_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.mount("/admin", admin_app)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug")
