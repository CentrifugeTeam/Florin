from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID
from .mixins import UUIDMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User

class Token(UUIDMixin, SQLModel, table=True):
    __tablename__ = 'tokens'
    token: str
    user_id: UUID = Field(foreign_key='users.id')
    user: 'User' = Relationship(back_populates='tokens')