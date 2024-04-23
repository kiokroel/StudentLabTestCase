from app import models
from app import schemas
from app.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


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


async def get_forms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Form).offset(skip).limit(limit).all()


async def create_user_form(db: Session, form: schemas.FormCreate, user_id: int):
    db_form = models.Form(**form.dict(), owner_id=user_id)
    db.add(db_form)
    await db.commit()
    await db.refresh(db_form)
    return db_form
