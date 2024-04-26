from app.services import forms as crud
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from app import schemas
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/forms",
    tags=["Формы"]
)


@router.get("{form_id}", response_model=schemas.FormGet)
async def read_form(form_id: int, session: AsyncSession = Depends(get_db)):
    form = await crud.get_form(session, form_id=form_id)
    if form is None:
        raise HTTPException(status_code=404, detail="User not found")
    return form


@router.post("", response_model=schemas.FormCreate)
async def create_form(user: schemas.UserCreate, session: AsyncSession = Depends(get_db)):
    user_from_db = await crud.get_user_by_email(session, email=user.email)
    if user_from_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await crud.create_user(session=session, user=user)
    return new_user


