from sqlmodel import SQLModel, Field
from fastapi import UploadFile
from sqlalchemy import String, Column, UniqueConstraint
from .mixins import UUIDMixin


class ProfileBase(SQLModel):
    username: str = Field(sa_column=Column(String(255), unique=True))
    email: str = Field(sa_column=Column(String(255), unique=True))

    __table_args__ = (UniqueConstraint('username', 'email'),)


class ProfileCreate(ProfileBase):
    password: str
    photo: UploadFile | None = None


class ProfileRead(UUIDMixin, ProfileBase):
    is_active: bool = True
    is_verified: bool = False
    is_superuser: bool = False
    photo_url: str | None = None
