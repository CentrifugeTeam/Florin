from sqlalchemy import Column, String, UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship
from .mixins import UUIDMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .tokens import Token


class User(UUIDMixin, SQLModel, table=True):
    __tablename__ = 'users'
    login: str
    password: str
    type: str

    username: str = Field(sa_column=Column(String(256), unique=True)) # if login in SSO give username like APP_USER_NAME
    email: str | None = None
    is_verified: bool = False
    photo_url: str | None = None

    __table_args__ = (UniqueConstraint('username'), )
    tokens: list['Token'] = Relationship(back_populates='user')
