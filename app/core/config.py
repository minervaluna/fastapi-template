# app/config.py
import os
from dotenv import load_dotenv

# load .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "FastAPI Project")
    API_ROUTE_PREFIX: str = os.getenv("API_ROUTE_PREFIX", "")
    # 从 .env 文件中读取数据库连接 URL，若无则默认使用 sqlite（开发调试时可用）
    SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    STORAGE_PATH: str = os.getenv("STORAGE_PATH", "./storage")

settings = Settings()
