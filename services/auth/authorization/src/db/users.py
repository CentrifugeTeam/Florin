from sqlalchemy import UniqueConstraint
from sqlmodel import Relationship

from ..schemas.users import UserRead
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .tokens import Token

class User(UserRead, table=True):
    password: str | None = None
    type: str
    
    tokens: list['Token'] = Relationship(back_populates='user')
    __table_args__ = (UniqueConstraint('username'), )



