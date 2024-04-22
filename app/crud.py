import models
import schemas
from sqlalchemy.orm import Session


async def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


async def get_user_by_email(db: Session, email: str):
    return (await db.query(models.User).filter(models.User.email == email)).first()


async def get_users(db: Session, skip: int = 0, limit: int = 100):
    return (await db.query(models.User).offset(skip).limit(limit)).all()


async def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_forms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Form).offset(skip).limit(limit).all()


async def create_user_form(db: Session, form: schemas.FormCreate, user_id: int):
    db_form = models.Form(**form.dict(), owner_id=user_id)
    db.add(db_form)
    await db.commit()
    await db.refresh(db_form)
    return db_form
