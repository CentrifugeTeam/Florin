from sqlmodel import SQLModel, Field, Relationship
from .mixins import UUIDMixin
from datetime import date
from uuid import UUID
from typing import TYPE_CHECKING


if TYPE_CHECKING:
  from families import Family
  from genius import Genius
  from ranks import Rank
  from plans import Plan
  from user_plants import UserPlant


class Plant(UUIDMixin, SQLModel, table=True):
  __tablename__ = 'plants'
  name: str
  bibliography: str
  slug: str
  year: date
  image_url: str = Field(default=None, nullable=True)


  family_id: UUID = Field(foreign_key='families.id')
  genius_id: UUID = Field(foreign_key='genius.id')
  rank_id: UUID = Field(foreign_key='ranks.id')
  plan_id: UUID = Field(foreign_key='plans.id')

  family: 'Family' = Relationship(back_populates='plants')
  genius: 'Genius' = Relationship(back_populates='plants')
  rank: 'Rank' = Relationship(back_populates='plants')
  plan: 'Plan' = Relationship(back_populates='plants')
  plant: 'UserPlant' = Relationship(back_populates='plant')



