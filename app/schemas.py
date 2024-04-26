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
        from_attributes = True


class FormGet(FormBase):
    pass
