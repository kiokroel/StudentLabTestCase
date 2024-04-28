from app import schemas, models
from app.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user(session: AsyncSession, user_id: int):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    return user


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    return user


async def create_user(session: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    session.add(db_user)
    await session.commit()
    return user
