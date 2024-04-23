from pydantic import BaseModel


class FieldBase(BaseModel):
    question: str
    type: str


class FormBase(BaseModel):
    name: str
    fields: tuple[FieldBase]


class FormCreate(FormBase):
    pass


class Form(FormBase):
    id: int
    is_published: bool
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    #forms: list[Form] = []

    class Config:
        orm_mode = True
