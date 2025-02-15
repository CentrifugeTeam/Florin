from fastapi import UploadFile

from sqlmodel import SQLModel, Field
from .mixins import UUIDMixin


class UserBase(SQLModel):
    __tablename__ = 'users'
    email: str



class UserCreate(UserBase):
    password: str
    photo: UploadFile | None = None

class UserRead(UUIDMixin, UserBase):
    username: str
    is_verified: bool = False
    photo_url: str | None = None


