from sqlmodel import SQLModel
from datetime import datetime
from ..plants.schema import PlantRead


class CalendarEvent(SQLModel):
    datetime: datetime
    plant: PlantRead
