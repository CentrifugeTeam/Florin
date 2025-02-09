from uuid import UUID

from sqlmodel import SQLModel, Field
from .mixins import UUIDMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

class Profile(UUIDMixin, SQLModel, table=True):
    __tablename__ = 'profiles'
    username: str
    email: str | None = None
    is_verified: bool = False
    photo_url: str | None = None

    account_id: UUID = Field(foreign_key='accounts.id')
