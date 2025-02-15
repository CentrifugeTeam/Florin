from fastapi import UploadFile
from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field
from .mixins import UUIDMixin


class UserBase(SQLModel):
    __tablename__ = 'users'
    email: str



class UserCreate(UserBase):
    password: str
    photo: UploadFile | None = None

class UserRead(UUIDMixin, UserBase):
    username: str = Field(sa_column=Column(String(256), unique=True, nullable=False))
    is_verified: bool = False
    photo_url: str | None = None



class Login(SQLModel):
    email: str
    password: str