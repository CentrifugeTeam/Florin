from sqlalchemy import Column, String
from uuid import UUID
from sqlmodel import SQLModel
from sqlmodel import Relationship, Field

from ..base.schema import UUIDMixin
from .schema import UserRead

class User(UUIDMixin, UserRead, table=True):
    password: str | None = None
    type: str
    username: str = Field(sa_column=Column(String(256), unique=True, nullable=False))
    email: str = Field(unique=True)

    tokens: list['Token'] = Relationship(back_populates='user')


class Token(UUIDMixin, SQLModel, table=True):
    __tablename__ = 'tokens'
    token: str
    user_id: UUID = Field(foreign_key='users.id')
    user: 'User' = Relationship(back_populates='tokens')