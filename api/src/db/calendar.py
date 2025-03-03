from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID
from sqlalchemy import Enum, Column, UniqueConstraint
from datetime import datetime
from .mixins import UUIDMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .plants import Plant
    from .user_plants import UserPlant


class CronPlantCalendarScheduler(UUIDMixin, SQLModel, table=True):
    __tablename__ = "cron_plant_calendar_scheduler"

    plant_id: UUID = Field(foreign_key="plants.id")
    cron_expression: str
    plant: "Plant" = Relationship(back_populates="cron_schedules")


class CalendarEvent(UUIDMixin, SQLModel, table=True):
    __tablename__ = "calendar_events"

    header: str
    content: str
    is_completed: bool = False
    do_on: datetime

    user_plant_id: UUID = Field(foreign_key="user_plants.id")

    user_plant: "UserPlant" = Relationship(back_populates="calendar_events")
    __table_args__ = (UniqueConstraint("do_on", "user_plant_id"),)
