from sqlmodel import SQLModel, Relationship
from .mixins import UUIDMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from .plants import Plant

class Family(UUIDMixin, SQLModel, table=True):
  __tablename__ = 'families'
  name: str

  plants: 'Plant' = Relationship(back_populates='family')