import json
from typing import List

from app import schemas, models
from app.models import Form, FormField, FormAnswer, FormResponse
from app.schemas import FormFieldBase
from sqlalchemy import select, update, delete
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


async def create_field(db: AsyncSession, field: schemas.FormFieldBase, form_id: int):
    options_str = json.dumps(field.options)
    db_field = models.FormField(name=field.name, field_type=field.field_type, options=options_str, form_id=form_id)
    db.add(db_field)
    await db.commit()
    await db.refresh(db_field)
    db_field.options = json.loads(db_field.options)
    return db_field


async def get_fields(db: AsyncSession, form_id: int):
    stmt = select(FormField).where(FormField.form_id == form_id)
    result = await db.execute(stmt)
    fields: List[FormField] | None = result.scalar()
    return fields


async def create_response(db: AsyncSession, form_id: int):
    db_response = models.FormResponse(form_id=form_id)
    db.add(db_response)
    await db.commit()
    await db.refresh(db_response)
    return db_response


async def create_answers(db: AsyncSession, answers: List[schemas.FormAnswerCreate], response_id: int):
    for answer in answers:
        selected_options_str = json.dumps(answer.selected_options)
        db_answer = models.FormAnswer(**answer.dict(), response_id=response_id)
        db_answer.selected_options = selected_options_str
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


async def delete_answer(db: AsyncSession, response_id: int):
    stmt = select(FormAnswer).where(FormAnswer.response_id == response_id)
    answers = await db.execute(stmt)
    for answer in answers:
        await db.delete(answer)
    await db.commit()


async def delete_response(db: AsyncSession, response_id: int):
    stmt = select(FormResponse).where(FormResponse.id == response_id)
    result = await db.execute(stmt)
    response: FormResponse | None = result.scalar_one_or_none()
    await db.delete(response)
    await db.commit()


async def delete_field(db: AsyncSession, form_id: int):
    stmt = select(FormField).where(FormField.form_id == form_id)
    fields = await db.execute(stmt)
    for field in fields:
        await db.delete(field)
    await db.commit()


async def delete_form(db: AsyncSession, form_id: int):
    form = await get_form(db, form_id=form_id)
    await db.delete(form)
    await db.commit()


async def get_responses(db: AsyncSession, form_id: int):
    stmt = select(FormResponse).where(FormResponse.form_id == form_id)
    result = await db.execute(stmt)
    responses: List[FormResponse] | None = result.scalar()
    for response in responses:
        for answer in response.answers:
            answer.selected_options = json.loads(answer.selected_options)
    return responses
