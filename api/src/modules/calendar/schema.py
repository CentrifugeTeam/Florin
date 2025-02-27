from sqlmodel import SQLModel
from datetime import datetime
from uuid import UUID
from typing import Union


class CalendarBase(SQLModel):
    rank: str
