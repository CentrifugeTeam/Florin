from uuid import UUID
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: UUID = Field(primary_key=True)



class Token(SQLModel, table=True):
    __tablename__ = 'tokens'
    id: UUID = Field(primary_key=True)
    user_id: UUID = Field(foreign_key='users.id')
    token: str
