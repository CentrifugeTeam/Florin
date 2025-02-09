
from sqlmodel import SQLModel
from .mixins import UUIDMixin


class Account(UUIDMixin, SQLModel, table=True):
    __tablename__ = 'accounts'
    login: str
    password: str
    type: str
    token: str