from app import schemas, models
from app.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user(db: AsyncSession, user_id: int):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    return user


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    return user


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    return user
