from ...deps import GetSession
from datetime import date
from fastapi_libkit.responses import ErrorModel, not_found_response, no_content_response
from sqlalchemy.orm import joinedload
from uuid import UUID
from fastapi import APIRouter, Query, Body, Response
from typing import Annotated
from .manager import calendar_manger
from .schema import PlantRead, PlantCard, NoteRead, UserPlantRead, UserPlantsProfile
from ..auth import to_openapi
from ..auth.authenticator import authenticate, UnauthorizedResponse
from ...db import Note, Plant, UserPlants

r = APIRouter(prefix='/calendar', tags=['Calendar'])


@r.get("", response_model=list[PlantRead])
async def calendar(session: GetSession, start_date: date, user: authenticate):
    user.plants.
    calendar_manger.get_new_events(start_date)
    # return await plant_manager.paginated_list(session, page, limit)
