from sqlmodel import Field
from sqlalchemy import Column, DateTime, text
from datetime import datetime
from uuid import UUID, uuid4


class UUIDMixin:
    id: UUID = Field(primary_key=True, default_factory=uuid4)


class TimestampMixin:
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    updated_at: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True, default=None, onupdate=text('CURRENT_TIMESTAMP')))