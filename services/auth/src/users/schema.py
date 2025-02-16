from fastapi import UploadFile
from pydantic import BaseModel
from sqlmodel import SQLModel

class UserBase(SQLModel):
    __tablename__ = 'users'
    email: str

class UserCreate(UserBase):
    password: str
    photo: UploadFile | None = None

class UserRead(UserBase):
    username: str
    is_verified: bool = False
    photo_url: str | None = None


class PermissionTokenRead(BaseModel):
    access_token: str
    token_type: str = 'bearer'
