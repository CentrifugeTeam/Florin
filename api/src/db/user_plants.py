from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint, Column, DateTime, text
from uuid import UUID
from .mixins import UUIDMixin, TimestampMixin
from datetime import date, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .plants import Plant
    from .calendar import CalendarEvent


class UserPlant(UUIDMixin, SQLModel, table=True):
    __tablename__ = "user_plants"
    name: str
    user_id: UUID = Field(foreign_key="users.id")
    plant_id: UUID = Field(foreign_key="plants.id")
    photo_url: str

    user: "User" = Relationship(back_populates="user_plants")
    plant: "Plant" = Relationship(back_populates="user_plants")

    calendar_events: list["CalendarEvent"] = Relationship(back_populates="user_plant")

    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
            onupdate=text("CURRENT_TIMESTAMP"),
        )
    )
