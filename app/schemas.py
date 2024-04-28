from datetime import datetime
from enum import Enum
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


class FormFieldBase(BaseModel):
    name: str
    field_type: str
    options: List[str] | None = None


class FormFieldGet(BaseModel):
    id: int


class FormGet(FormBase):
    id: int
    is_published: bool
    fields: None | List[FormFieldBase]


class FormAnswerBase(BaseModel):
    field_id: int
    text_answer: str | None = None
    selected_option: str | None = None
    selected_options: List[str] | None = None


class FormAnswerCreate(FormAnswerBase):
    pass


class FormResponseGet(BaseModel):
    form_id: int
    answers: None | List[FormAnswerCreate] = None


class FormResponses(FormResponseGet):
    response_time: datetime
    pass
