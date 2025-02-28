from fastapi import UploadFile
from uuid import UUID
from pydantic import BaseModel
from sqlmodel import SQLModel


class UserBase(SQLModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str
    photo: UploadFile | None = None


class UserRead(UserBase):
    id: UUID
    is_verified: bool = False
    photo_url: str | None = None


class UserUpdate(SQLModel):
    username: str


class PermissionTokenRead(BaseModel):
    access_token: str
    token_type: str = 'bearer'
