"""database connection module"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config_data.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


engine = create_async_engine(
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

Base = declarative_base()
Async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
session = Async_session()
