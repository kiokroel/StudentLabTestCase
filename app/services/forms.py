from typing import List

from app import schemas, models
from app.models import Form, FormResponse
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


async def get_form(db: AsyncSession, form_id: int):
    stmt = select(Form).where(Form.id == form_id)
    result = await db.execute(stmt)
    form: Form | None = result.scalar_one_or_none()
    return form


async def create_form(db: AsyncSession, form: schemas.FormCreate, creator_id: int):
    db_form = models.Form(**form.dict(), creator_id=creator_id)
    db.add(db_form)
    await db.commit()
    await db.refresh(db_form)
    return db_form


async def create_options(db: AsyncSession, options: List[str], field_id: int):
    for option in options:
        db_option = models.FormFieldOption(field_id=field_id, option=option)
        db.add(db_option)
    await db.commit()
        

async def create_field(db: AsyncSession, field: schemas.FormFieldCreate, form_id: int, field_type: str):
    db_field = models.FormField(name=field.name, field_type=field_type, form_id=form_id)
    db.add(db_field)
    await db.commit()
    await db.refresh(db_field)
    await create_options(db, field.options, field_id=db_field.id)
    await db.refresh(db_field)
    return db_field


async def create_response(db: AsyncSession, form_id: int):
    db_response = models.FormResponse(form_id=form_id)
    db.add(db_response)
    await db.commit()
    await db.refresh(db_response)
    return db_response


async def create_answers(db: AsyncSession, answers: List[schemas.FormAnswerCreate], response_id: int):
    for answer in answers:
        db_answer = models.FormAnswer(**answer.dict(), response_id=response_id)
        db.add(db_answer)
    await db.commit()


async def publish_form(db: AsyncSession, form_id: int):
    stmt = (
        update(Form).
        where(Form.id == form_id).
        values(is_published=True)
    )
    await db.execute(stmt)


async def unpublish_form(db: AsyncSession, form_id: int):
    stmt = (
        update(Form).
        where(Form.id == form_id).
        values(is_published=False)
    )
    await db.execute(stmt)


async def delete_form(db: AsyncSession, form_id: int):
    form = await get_form(db, form_id=form_id)
    await db.delete(form)
    await db.commit()
    return form


async def get_responses(db: AsyncSession, form_id: int):
    stmt = select(FormResponse).where(FormResponse.form_id == form_id)
    result = await db.execute(stmt)
    responses: List[FormResponse] | None = result.scalars().all()
    return responses
