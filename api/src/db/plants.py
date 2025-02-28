from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint, Column, DateTime, text
from uuid import UUID
from .mixins import UUIDMixin, TimestampMixin
from datetime import date, datetime
from typing import TYPE_CHECKING
from .user_plants import UserPlant

if TYPE_CHECKING:
    from .users import User
    from .calendar import CronPlantCalendarScheduler


class Plant(UUIDMixin, SQLModel, table=True):
    __tablename__ = "plants"
    name: str = Field(unique=True)
    bibliography: str
    slug: str
    year: date
    image_url: str
    family: str
    genus: str
    rank: str

    note: 'Note' = Relationship(back_populates='plant')
    user_plants: list['UserPlant'] = Relationship(back_populates='plant')
    cron_schedules: list['CronPlantCalendarScheduler'] = Relationship(
        back_populates='plant')


class Note(UUIDMixin, TimestampMixin, SQLModel, table=True):
    __tablename__ = "notes"
    plant_id: UUID = Field(foreign_key="plants.id")
    user_id: UUID = Field(foreign_key="users.id")
    text: str
    plant: 'Plant' = Relationship(back_populates='note')

    __table_args__ = (UniqueConstraint('plant_id', 'user_id'),)
