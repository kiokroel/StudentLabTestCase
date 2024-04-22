from app import crud
from app.main import get_db
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
import schemas
from sqlalchemy.orm import Session

#from repository import FormsRepository
#from schemas import Form

router = APIRouter(
    prefix="/forms",
    tags=["Формы"]
)


@router.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

'''@router.post("/")
async def add_form(
        form: Annotated[Form, Depends()]):
    form_id = await FormsRepository.add_one(form)
    return {"ok": True, "id": form_id}'''


'''@router.get("/{form_id}", response_model=Form)
def get_form():
    form = Form(name="qweqwqw")
    return form'''
