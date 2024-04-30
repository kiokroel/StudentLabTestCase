from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class FormBase(BaseModel):
    title: str
    description: str | None = None


class FormCreate(FormBase):
    pass


class FormFieldOptionBase(BaseModel):
    option: str


class FormFieldBase(BaseModel):
    name: str


class FormFieldCreate(FormFieldBase):
    options: List[str]


class FormFieldGet(FormFieldBase):
    id: int
    field_type: str
    options: List[FormFieldOptionBase] | None = None


class FormGet(FormBase):
    id: int
    is_published: bool
    fields: None | List[FormFieldGet]


class FormAnswerBase(BaseModel):
    field_id: int
    answer: str | None = None


class FormAnswerCreate(FormAnswerBase):
    pass


class FormAnswerGet(FormAnswerBase):
    field: FormFieldGet


class FormResponseGet(BaseModel):
    form_id: int
    answers: None | List[FormAnswerGet] = None


class FormResponses(FormResponseGet):
    response_time: datetime
