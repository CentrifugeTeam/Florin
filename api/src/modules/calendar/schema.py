from sqlmodel import SQLModel
from uuid import UUID
from datetime import datetime
from ..plants.schema import PlantRead, UserPlantRead


class CalendarEventRead(SQLModel):
    id: UUID
    header: str
    content: str
    do_on: datetime
    is_completed: bool
    user_plant: UserPlantRead
