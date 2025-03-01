from sqlmodel import SQLModel, Relationship, Field
from .mixins import UUIDMixin
from typing import TYPE_CHECKING
from sqlalchemy import Column, DateTime, text
from datetime import datetime
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from .plants import Plant


class Article(UUIDMixin, SQLModel, table=True):
    __tablename__ = "articles"
    text: str

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

    plant_id: UUID = Field(foreign_key="plants.id")
    plant: "Plant" = Relationship(back_populates="articles")
