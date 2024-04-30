from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean, LargeBinary
from sqlalchemy.orm import relationship, Mapped

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(30), unique=True, nullable=False, index=True)
    username = Column(String(30), nullable=False, index=True)
    password = Column(LargeBinary, nullable=False)
    date_registration = Column(TIMESTAMP, default=datetime.utcnow)


class Form(Base):
    __tablename__ = "forms"

    id = Column(Integer, primary_key=True)
    title = Column(String(20), index=True)
    description = Column(String)
    creator_id = Column(Integer, ForeignKey("users.id"))
    is_published = Column(Boolean, default=False)
    data_create = Column(TIMESTAMP, default=datetime.utcnow)
    data_change = Column(TIMESTAMP, default=datetime.utcnow)

    fields: Mapped[List["FormField"]] = relationship("FormField", back_populates="form", lazy="selectin",
                                                     cascade='all, delete', passive_deletes=True)
    responses: Mapped[List["FormResponse"]] = relationship("FormResponse", back_populates="form", lazy="selectin",
                                                           cascade='all, delete', passive_deletes=True)


class FormField(Base):
    __tablename__ = "form_fields"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    field_type = Column(String)
    form_id = Column(Integer, ForeignKey("forms.id"))

    options = relationship("FormFieldOption", back_populates="field", lazy="selectin", cascade='all, delete',
                           passive_deletes=True)
    form = relationship("Form", back_populates="fields")
    answers = relationship('FormAnswer', back_populates="field", lazy="selectin", cascade='all, delete',
                           passive_deletes=True)


class FormFieldOption(Base):
    __tablename__ = "form_field_options"

    id = Column(Integer, primary_key=True)
    field_id = Column(Integer, ForeignKey("form_fields.id"))
    option = Column(String)

    field = relationship("FormField", back_populates="options")


class FormResponse(Base):
    __tablename__ = "form_responses"

    id = Column(Integer, primary_key=True)
    form_id = Column(Integer, ForeignKey("forms.id"))
    response_time = Column(TIMESTAMP, default=datetime.utcnow, index=True)

    answers: Mapped[List["FormAnswer"]] = relationship("FormAnswer", back_populates="response", lazy="selectin",
                                                       cascade='all, delete', passive_deletes=True)
    form = relationship("Form", back_populates="responses")


class FormAnswer(Base):
    __tablename__ = "form_answers"

    id = Column(Integer, primary_key=True)
    field_id = Column(Integer, ForeignKey("form_fields.id"))
    response_id = Column(Integer, ForeignKey("form_responses.id"))
    answer = Column(String, nullable=True)

    response = relationship("FormResponse", back_populates="answers")
    field = relationship("FormField", back_populates="answers", lazy="selectin")
