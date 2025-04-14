# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 如果使用 sqlite，则加入额外参数，否则不需要
if "sqlite" in settings.SQLALCHEMY_DATABASE_URL:
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URL,
        pool_size=10,  # 设置连接池中的连接数
        max_overflow=20,  # 设置超出 pool_size 后最多可以创建的连接数
        pool_recycle=3600  # 设置连接回收时间，防止长时间连接导致的问题
    )
else:
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
