from sqlmodel import Field, Relationship
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User

from sqlmodel import SQLModel
from ..schemas.mixins import UUIDMixin

class Token(UUIDMixin, SQLModel, table=True):
    __tablename__ = 'tokens'
    token: str
    user_id: UUID = Field(foreign_key='users.id')
    user: 'User' = Relationship(back_populates='tokens')