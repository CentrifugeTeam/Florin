from uuid import UUID

from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field

from .mixins import UUIDMixin


class Role(UUIDMixin, SQLModel, table=True):
    __tablename__ = 'roles'
    name: str = Field(sa_column=Column(String(256), unique=True))


class ProfileRole(UUIDMixin, SQLModel, table=True):
    __tablename__ = 'user_roles'
    profile_id: UUID = Field(foreign_key='profiles.id')
    role_id: UUID = Field(foreign_key='roles.id')
