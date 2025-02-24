from sqlalchemy import Column, String, UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship
from .mixins import UUIDMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .tokens import Token
    from user_plants import UserPlant


class User(UUIDMixin, SQLModel, table=True):
    __tablename__ = 'users'
    password: str | None
    type: str
    username: str = Field(sa_column=Column(String(256), nullable=False)) # if login in SSO give username like APP_USER_NAME
    email: str
    is_verified: bool = False
    photo_url: str | None = None

    tokens: list['Token'] = Relationship(back_populates='user')
    user: 'UserPlant' = Relationship(back_populates='user')

