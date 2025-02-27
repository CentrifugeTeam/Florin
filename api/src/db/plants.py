from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint, Column, DateTime, text
from uuid import UUID
from .mixins import UUIDMixin, TimestampMixin
from datetime import date, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User


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
    user_plants: list['UserPlants'] = Relationship(back_populates='plant')
    # users: list['User'] = Relationship( #TODO fix it need to create link model
    # back_populates='plants', link_model='user_plants')


class Note(UUIDMixin, TimestampMixin, SQLModel, table=True):
    __tablename__ = "notes"
    plant_id: UUID = Field(foreign_key="plants.id")
    user_id: UUID = Field(foreign_key="users.id")
    text: str
    plant: 'Plant' = Relationship(back_populates='note')

    __table_args__ = (UniqueConstraint('plant_id', 'user_id'),)


class UserPlants(UUIDMixin, SQLModel, table=True):
    __tablename__ = "user_plants"
    name: str
    user_id: UUID = Field(foreign_key="users.id")
    plant_id: UUID = Field(foreign_key="plants.id")

    plant: 'Plant' = Relationship(back_populates='user_plants')

    created_at: datetime = Field(sa_column=Column(DateTime(
        timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    updated_at: datetime = Field(sa_column=Column(
        DateTime(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP')))
