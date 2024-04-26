from config import DATABASE_URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = DATABASE_URL

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = async_sessionmaker(engine)

Base = declarative_base()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
