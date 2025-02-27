from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID
from sqlalchemy import Enum, Column
from datetime import datetime
from .mixins import UUIDMixin
from enum import StrEnum, auto


class SeasonTypes(StrEnum):
    winter = auto()
    summer = auto()
    autumn = auto()
    spring = auto()


class CronPlantCalendarScheduler(UUIDMixin, SQLModel, table=True):
    __tablename__ = "cron_plant_calendar_scheduler"

    plant_id: UUID = Field(foreign_key="plants.id")
    start_datetime: datetime
    cron_expression: str
    season_type: SeasonTypes = Field(sa_column=Column(
        Enum(SeasonTypes),
        nullable=False,
    ))
