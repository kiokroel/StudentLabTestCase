import os

from config import DATABASE_URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

SQLALCHEMY_DATABASE_URL = DATABASE_URL

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = async_sessionmaker(engine)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
