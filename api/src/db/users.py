from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import SQLModel, Field, Relationship
from .mixins import UUIDMixin
from uuid import UUID
from typing import TYPE_CHECKING
from .user_plants import UserPlant

if TYPE_CHECKING:
    from .plants import Plant


class User(AsyncAttrs, UUIDMixin, SQLModel, table=True):
    __tablename__ = "users"
    password: str | None
    type: str
    # if login in SSO give username like APP_USER_NAME
    username: str = Field(sa_column=Column(String(256), nullable=False))
    email: str = Field(unique=True)
    is_verified: bool = False
    is_superuser: bool = False
    photo_url: str | None = None

    user_plants: list["UserPlant"] = Relationship(back_populates="user")
    # plants: list['Plant'] = Relationship(
    # back_populates='users', link_model=UserPlant)


class Role(UUIDMixin, SQLModel, table=True):
    __tablename__ = "roles"
    name: str
    # users: list['User'] = Relationship(back_populates='role')


class Token(UUIDMixin, SQLModel, table=True):
    __tablename__ = "tokens"
    token: str
    user_id: UUID = Field(foreign_key="users.id")
    UniqueConstraint("token", "user_id", name="unique_token_user")


class UserRole(UUIDMixin, SQLModel, table=True):
    __tablename__ = "user_roles"
    user_id: UUID = Field(foreign_key="users.id")
    role_id: UUID = Field(foreign_key="roles.id")
