from fastapi import UploadFile
from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field
from .mixins import UUIDMixin


class UserBase(SQLModel):
    __tablename__ = 'users'
    email: str | None = None



class UserCreate(UserBase):
    login: str
    password: str
    photo: UploadFile | None = None
    password: str

class UserRead(UUIDMixin, UserBase):
    username: str = Field(
        sa_column=Column(String(256), unique=True))  # if login in SSO give username like APP_USER_NAME
    is_verified: bool = False
    photo_url: str | None = None

