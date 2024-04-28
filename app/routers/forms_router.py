import json
from typing import List

from app.schemas import FormResponses
from app.services import forms as crud
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from app import schemas
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/forms",
    tags=["Формы"]
)


async def is_authorized(db, form_id, user_id):
    form = await crud.get_form(db, form_id=form_id)
    if form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    if form.creator_id is not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return form


@router.get("/{form_id}", response_model=schemas.FormGet)
async def get_form(form_id: int, db: AsyncSession = Depends(get_db)):
    form = await crud.get_form(db, form_id=form_id)
    if form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    for field in form.fields:
        field.options = json.loads(field.options)
    return form


@router.post("", response_model=schemas.FormGet)
async def create_form(form: schemas.FormCreate, creator_id: int, db: AsyncSession = Depends(get_db)):
    new_form = await crud.create_form(db=db, form=form, creator_id=creator_id)
    return new_form


@router.post("/{form_id}/fields", response_model=schemas.FormFieldBase)
async def add_field(field: schemas.FormFieldBase, form_id: int, db: AsyncSession = Depends(get_db)):
    form = await crud.get_form(db, form_id=form_id)
    if form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    return await crud.create_field(db=db, field=field, form_id=form_id)


@router.post("/{form_id}/responses", response_model=schemas.FormResponseGet)
async def create_form_response(answers: List[schemas.FormAnswerCreate], form_id: int, db: AsyncSession = Depends(get_db)):
    form = await crud.get_form(db, form_id=form_id)
    if form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    response = await crud.create_response(db, form_id=form_id)
    await crud.create_answers(db, answers=answers, response_id=response.id)
    await db.refresh(response)
    for answer in response.answers:
        answer.selected_options = json.loads(answer.selected_options)
    return response


@router.patch("/{form_id}/publish", response_model=schemas.FormGet)
async def publish_form(form_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    form = await is_authorized(db, user_id=user_id, form_id=form_id)
    await crud.publish_form(db, form_id=form_id)
    await db.refresh(form)
    for field in form.fields:
        field.options = json.loads(field.options)
    return form


@router.patch("/{form_id}/unpublish", response_model=schemas.FormGet)
async def unpublish_form(form_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    form = await is_authorized(db, user_id=user_id, form_id=form_id)
    if form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    if form.creator_id is not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    await crud.unpublish_form(db, form_id=form_id)
    await db.refresh(form)
    for field in form.fields:
        field.options = json.loads(field.options)
    return form


@router.delete("/{form_id}/delete", response_model=schemas.FormGet)
async def delete_form(form_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    form = await is_authorized(db, form_id=form_id, user_id=user_id)
    await crud.delete_form(db, form_id=form_id)
    for field in form.fields:
        field.options = json.loads(field.options)
    return form


@router.get("/{form_id}/answers", response_model=List[FormResponses])
async def get_responses(form_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    await is_authorized(db, form_id=form_id, user_id=user_id)
    responses = await crud.get_responses(db, form_id=form_id)
    return responses
