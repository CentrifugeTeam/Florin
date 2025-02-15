from uuid import UUID
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: UUID = Field(primary_key=True)

