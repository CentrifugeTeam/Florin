from sqlalchemy import Column, String, UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship
from .mixins import UUIDMixin
from uuid import UUID


class User(UUIDMixin, SQLModel, table=True):
    __tablename__ = 'users'
    password: str | None
    type: str
    username: str = Field(sa_column=Column(String(256), nullable=False)) # if login in SSO give username like APP_USER_NAME
    email: str
    is_verified: bool = False
    is_superuser: bool = False
    photo_url: str | None = None
    tokens: list['Token'] = Relationship(back_populates='user')
    

class Token(UUIDMixin, SQLModel, table=True):
    __tablename__ = 'tokens'
    token: str
    user_id: UUID = Field(foreign_key='users.id')
    user: 'User' = Relationship(back_populates='tokens')
    

class Role(UUIDMixin, SQLModel, table=True):
    __tablename__ = 'roles'
    name: str
    users: list['User'] = Relationship(back_populates='role')
    
class UserRole(UUIDMixin, SQLModel, table=True):
    __tablename__ = 'user_roles'
    user_id: UUID = Field(foreign_key='users.id')
    role_id: UUID = Field(foreign_key='roles.id')
    