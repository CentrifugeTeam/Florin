from sqlalchemy import UniqueConstraint
from sqlalchemy import Column, String
from sqlmodel import Relationship, Field

from ..schemas.users import UserRead
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .tokens import Token

class User(UserRead, table=True):
    password: str | None = None
    type: str
    username: str = Field(sa_column=Column(String(256), unique=True, nullable=False))
    email: str = Field(unique=True)

    tokens: list['Token'] = Relationship(back_populates='user')



