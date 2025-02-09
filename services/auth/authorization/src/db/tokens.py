from sqlmodel import Field, Relationship
from uuid import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User

from ..schemas.tokens import PermissionTokenRead
from ..schemas.mixins import UUIDMixin

class Token(UUIDMixin, PermissionTokenRead, table=True):
    __tablename__ = 'tokens'
    user_id: UUID = Field(foreign_key='users.id')
    user: 'User' = Relationship(back_populates='tokens')