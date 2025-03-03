from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID
from datetime import date
from typing import Union


class PlantBase(SQLModel):
    name: str | None = Field(description="Имя растения на русском языке")
    origin_name: str = Field(description="Оригинальное имя")
    bibliography: str
    slug: str
    year: date
    image_url: str
    family: str
    genus: str
    rank: str


class PlantRead(PlantBase):
    id: UUID


class PlantCard(PlantRead):
    note: Union["NoteRead", None]


class NoteRead(SQLModel):
    id: UUID
    text: str
    plant_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class UserPlantRead(SQLModel):
    id: UUID
    name: str
    photo_url: str
    plant_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class UserPlantsProfile(SQLModel):
    id: UUID
    name: str
    plant: "PlantRead"
    created_at: datetime
    updated_at: datetime
