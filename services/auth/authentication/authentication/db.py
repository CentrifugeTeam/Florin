from sqlmodel import SQLModel

class User(SQLModel, table=True):
    __tablename__ = 'users'

