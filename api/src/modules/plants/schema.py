from sqlmodel import SQLModel
from datetime import datetime
from uuid import UUID
from typing import Union


class PlantBase(SQLModel):
    name: str
    bibliography: str
    slug: str
    # year: str
    image_url: str
    family: str
    genus: str
    rank: str


class PlantRead(PlantBase):
    id: UUID


class PlantCard(PlantRead):
    note: Union['NoteRead', None]


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
    plant_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class UserPlantsProfile(SQLModel):
    id: UUID
    name: str
    plant: 'PlantRead'
    created_at: datetime
    updated_at: datetime
