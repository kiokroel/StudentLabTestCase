from app.services import users as crud
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from app import schemas
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)


@router.post("", response_model=schemas.UserCreate)
async def create_user(user: schemas.UserCreate, session: AsyncSession = Depends(get_db)):
    user_from_db = await crud.get_user_by_email(session, email=user.email)
    if user_from_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await crud.create_user(session=session, user=user)
    return new_user


@router.get("{user_id}", response_model=schemas.UserCreate)
async def read_user(user_id: int, session: AsyncSession = Depends(get_db)):
    user = await crud.get_user(session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
