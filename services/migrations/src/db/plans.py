from sqlmodel import SQLModel, Relationship
from .mixins import UUIDMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from .plants import Plant

class Plan(UUIDMixin, SQLModel, table=True):
  __tablename__ = 'plans'
  day: int
  action: str

  plants: 'Plant' = Relationship(back_populates='plan')