from enum import Enum
from typing import List, Literal

from app.schemas import FormResponses, User
from app.services import forms as crud
from auth.auth_router import get_current_auth_user
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from app import schemas
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/forms",
    tags=["Формы"]
)


async def is_authorized(db, form_id, user_id) -> Literal[True]:
    form = await crud.get_form(db, form_id=form_id)
    if form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    if form.creator_id != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True


@router.get("/{form_id}", response_model=schemas.FormGet)
async def get_form(form_id: int, db: AsyncSession = Depends(get_db)):
    form = await crud.get_form(db, form_id=form_id)
    if form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    return form


@router.get("/", response_model=List[schemas.FormGet])
async def get_my_forms(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_auth_user)):
    forms = await crud.get_forms_by_user(db, user_id=user.id)
    if forms is None:
        raise HTTPException(status_code=404, detail="Form not found")
    return forms


@router.post("", response_model=schemas.FormGet)
async def create_form(form: schemas.FormCreate = Depends(), db: AsyncSession = Depends(get_db),
                      user: User = Depends(get_current_auth_user)):
    creator_id = user.id
    new_form = await crud.create_form(db=db, form=form, creator_id=creator_id)
    return new_form


class TypeField(str, Enum):
    text = "text",
    radio_button = "radio_button",
    checkbox_button = "checkbox_button"


@router.post("/{form_id}/fields", response_model=schemas.FormFieldGet)
async def add_field(field: schemas.FormFieldCreate, field_type: TypeField, form_id: int,
                    db: AsyncSession = Depends(get_db),
                    user: User = Depends(get_current_auth_user)):
    if field_type == TypeField.text:
        field.options = []
    if await is_authorized(db, form_id=form_id, user_id=user.id):
        return await crud.create_field(db=db, field=field, form_id=form_id, field_type=field_type)


@router.post("/{form_id}/responses", response_model=schemas.FormResponseGet)
async def create_form_response(answers: List[schemas.FormAnswerCreate], form_id: int,
                               db: AsyncSession = Depends(get_db)):
    form = await crud.get_form(db, form_id=form_id)
    if form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    response = await crud.create_response(db, form_id=form_id)
    await crud.create_answers(db, answers=answers, response_id=response.id)
    await db.refresh(response)
    return response


@router.patch("/{form_id}/publish", response_model=schemas.FormGet)
async def publish_form(form_id: int, db: AsyncSession = Depends(get_db),
                       user: User = Depends(get_current_auth_user)):
    if await is_authorized(db, user_id=user.id, form_id=form_id):
        await crud.publish_form(db, form_id=form_id)
        return await crud.get_form(db, form_id=form_id)


@router.patch("/{form_id}/unpublish", response_model=schemas.FormGet)
async def unpublish_form(form_id: int, db: AsyncSession = Depends(get_db),
                         user: User = Depends(get_current_auth_user)):
    if await is_authorized(db, user_id=user.id, form_id=form_id):
        await crud.unpublish_form(db, form_id=form_id)
        return await crud.get_form(db, form_id=form_id)


@router.delete("/{form_id}/delete", response_model=schemas.FormGet)
async def delete_form(form_id: int, db: AsyncSession = Depends(get_db),
                      user: User = Depends(get_current_auth_user)):
    if await is_authorized(db, form_id=form_id, user_id=user.id):
        return await crud.delete_form(db, form_id=form_id)


@router.get("/{form_id}/answers", response_model=List[FormResponses])
async def get_responses(form_id: int, db: AsyncSession = Depends(get_db),
                        user: User = Depends(get_current_auth_user)):
    if await is_authorized(db, form_id=form_id, user_id=user.id):
        responses = await crud.get_responses(db, form_id=form_id)
        return responses
