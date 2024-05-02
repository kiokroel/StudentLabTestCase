from config import DB_USER, DB_PORT, DB_PASS, DB_NAME, DB_HOST
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

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
