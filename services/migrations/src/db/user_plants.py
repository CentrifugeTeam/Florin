from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID
from .mixins import UUIDMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from .users import User
  from .plants import Plant

class UserPlant(UUIDMixin, SQLModel, table=True):
  __tablename__ = 'user_plants'
  user_id: UUID = Field(foreign_key='users.id')
  plant_id: UUID = Field(foreign_key='plants.id')

  user: 'User' = Relationship(back_populates='user')
  plant: 'Plant' = Relationship(back_populates='plant')