from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID
from sqlalchemy import Enum, Column
from datetime import datetime
from .mixins import UUIDMixin
from enum import StrEnum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .plants import Plant


class SeasonTypes(StrEnum):
    winter = auto()
    summer = auto()
    autumn = auto()
    spring = auto()


class CronPlantCalendarScheduler(UUIDMixin, SQLModel, table=True):
    __tablename__ = "cron_plant_calendar_scheduler"

    plant_id: UUID = Field(foreign_key="plants.id")
    cron_expression: str
    season_type: SeasonTypes = Field(sa_column=Column(
        Enum(SeasonTypes),
        nullable=False,
    ))

    plant: 'Plant' = Relationship(back_populates='cron_schedules')
