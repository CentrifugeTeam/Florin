from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID
from datetime import date
from typing import Union
from ..plants.schema import PlantRead


class ArticleBase(SQLModel):
    text: str
    created_at: datetime
    updated_at: datetime


class ArticleRead(ArticleBase):
    id: UUID
    plant: PlantRead
