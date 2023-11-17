"""
Configuration file
"""


import os


# pylint: disable=too-few-public-methods
class Settings:
    """
    Settings class
    """

    MODULE_LIST: list = [
        "models.user",
        "models.wishlist",
        "models.admin",
    ]

    ALLOWED_CONTENT_TYPES: list = [
        "image/png",
        "image/jpeg",
        "image/jpg",
        "image/webp",
    ]
    IMAGE_MAX_SIZE = 1.5 * 1024 * 1024
    DEFAULT_IMAGE_URL = (
        "https://firebasestorage.googleapis.com/v0/b/"
        "wishlist-f1b1e.appspot.com/o/mqdefault.jpeg?alt=media"
    )

    PROJECT_NAME: str = "Wishlist"
    PROJECT_VERSION: str = "0.0.1"

    USER: str = os.getenv("USER", default="admin")
    PASSWORD = os.getenv("PASSWORD", default="123456")
    SERVER: str = os.getenv("SERVER", default="localhost")
    PORT: str = os.getenv("PORT", default="3306")
    DB: str = os.getenv("DB", default="tdd")
    DATABASE_URL = f"mysql://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB}"

    SECRET_KEY: str = os.getenv("SECRET_KEY", default="AWESOME_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRATION = 1800
    JWT_REFRESH_TOKEN_EXPIRATION = 2592000
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


settings = Settings()
