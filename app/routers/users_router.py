from app.services import users as crud
from auth.utils import hash_password
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from app import schemas
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)


@router.post("", response_model=schemas.User)
async def create_user(user: schemas.UserCreate = Depends(), db: AsyncSession = Depends(get_db)):
    user_from_db = await crud.get_user_by_email(db, email=user.email)
    if user_from_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = hash_password(user.password)
    new_user = await crud.create_user(db=db, user=user)
    return new_user


@router.get("/{user_id}", response_model=schemas.UserBase)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
