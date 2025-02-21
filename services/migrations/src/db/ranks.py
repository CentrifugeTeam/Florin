from sqlmodel import SQLModel, Relationship
from .mixins import UUIDMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from .plants import Plant

class Rank(UUIDMixin, SQLModel, table=True):
  __tablename__ = 'ranks'
  name: str

  plants: 'Plant' = Relationship(back_populates='rank')