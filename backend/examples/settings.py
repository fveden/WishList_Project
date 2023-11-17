import os

from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "mysql://root:12345@localhost:3306/fastapi_admin")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")