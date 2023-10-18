"""
Main file
"""


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from api.routes import router
from auth.routes import auth_router
from config import settings

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
    await Tortoise.init(
        db_url=settings.DATABASE_URL, modules={"models": ["models.item", "models.user"]}
    )


@app.on_event("shutdown")
async def shutdown_db():
    """
    Shutdown method
    """
    await Tortoise.close_connections()


app.include_router(router, prefix="/api")
app.include_router(auth_router, prefix="/api")
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
