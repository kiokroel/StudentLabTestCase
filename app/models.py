from datetime import datetime

from sqlalchemy import MetaData, Column, Integer, String, TIMESTAMP, Table, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, nullable=False, index=True)
    password = Column(String, nullable=False)
    date_registration = Column(TIMESTAMP, default=datetime.utcnow)

    forms = relationship("Form", back_populates="owner")


class Form(Base):
    __tablename__ = "forms"

    id = Column(Integer, primary_key=True)
    name = Column(String, )
    creator = Column(Integer, ForeignKey("users.id"))
    is_published = Column(Boolean, default=False)
    data_create = Column(TIMESTAMP, default=datetime.utcnow)
    data_change = Column(TIMESTAMP, default=datetime.utcnow)

    owner = relationship("User", back_populates="forms")
    questions = relationship("Question", back_populates="form")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    text = Column(String, default=None)
    form = Column(Integer, ForeignKey("forms.id"))


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("users.id"))
    form = Column(Integer, ForeignKey("forms.id"))


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    result = Column(Integer, ForeignKey("answers.id"))
    answer = Column(String)

