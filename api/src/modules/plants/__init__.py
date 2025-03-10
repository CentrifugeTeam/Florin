import json
from ...deps import GetRedis, GetSession
from fastapi_libkit.responses import ErrorModel, not_found_response, no_content_response
from sqlalchemy.orm import joinedload
from uuid import UUID
from fastapi import APIRouter, Query, Body, Request, Response, Depends, HTTPException, UploadFile
from typing import Annotated
from datetime import datetime, timedelta, date
from ..files.adapter import file_adapter
from .schema import PlantRead, PlantCard, NoteRead, UserPlantRead, UserPlantsProfile
from ..calendar.manager import calendar_manager
from ...responses import to_openapi
from .manager import user_plant_manager, plant_manager
from ..auth.authenticator import authenticated, UnauthorizedResponse, authenticator
from ...db import Note, Plant, UserPlant, CalendarEvent, User

r = APIRouter(prefix="/plants", tags=["Plants"])


@r.get("", response_model=list[PlantRead])
async def plants(
    session: GetSession,
    limit: Annotated[int, Query(gt=0)] = 10,
    page: Annotated[int, Query(gt=0)] = 1,
):
    return await plant_manager.paginated_list(session, page, limit)


@r.get(
    "/{id}",
    response_model=PlantCard,
    responses={404: {"model": ErrorModel, "detail": "Not found"}},
)
async def plant(session: GetSession, id: UUID):
    return await plant_manager.get_or_404(
        session, id=id, options=joinedload(Plant.note)
    )


@r.post(
    "/{id}/note",
    response_model=NoteRead,
    responses={
        404: {"model": ErrorModel, "detail": "Not found"},
        **to_openapi(UnauthorizedResponse),
    },
)
async def plant_note(
    session: GetSession,
    id: UUID,
    user: authenticated,
    text: Annotated[str, Body(embed=True)],
):
    plant = await plant_manager.get_or_404(session, id=id)
    note = Note(user_id=user.id, plant_id=plant.id, text=text)
    session.add(note)
    await session.commit()
    return note


@r.post(
    "/{id}/attach",
    response_model=UserPlantRead,
    responses={**not_found_response, **to_openapi(UnauthorizedResponse)},
)
async def my_plants(
    *,
    id: UUID,
    session: GetSession,
    name: Annotated[str | None, Body(embed=True)] = None,
    user: authenticated,
):
    plant = await session.get(Plant, id, options=[joinedload(Plant.cron_schedules)])
    if not plant:
        raise HTTPException(status_code=404)

    user_plant = UserPlant(
        photo_url="",
        name=name or plant.name or plant.origin_name,
        user_id=user.id,
        plant_id=plant.id,
    )
    session.add(user_plant)

    # create new calendar events in two months for this plant
    start_date = datetime.now()
    month = start_date.month % 12 + 2
    year = start_date.year + (month // 12)
    end_date = datetime(year=year, month=month, day=1)
    for new_datetime in calendar_manager.get_new_datetime_in_interval(
        start_date, end_date, plant.cron_schedules[0]
    ):
        event = CalendarEvent(
            do_on=new_datetime,
            user_plant_id=user_plant.id,
            header="Полив растения",
            content=f"Успей полить растение {plant.name or plant.origin_name}",
        )
        session.add(event)
    await session.commit()

    return user_plant


@r.get(
    "/attached/",
    response_model=list[UserPlantsProfile],
    responses={**to_openapi(UnauthorizedResponse)},
)
async def attach(session: GetSession, user: authenticated):
    return await user_plant_manager.paginated_list(session, user)


@r.delete(
    "/{id}/detach",
    responses={
        **not_found_response,
        **to_openapi(UnauthorizedResponse),
        **no_content_response,
    },
)
async def detach(
    session: GetSession,
    id: UUID,
    user: authenticated,
):
    """Удалить прикреплённый цветок"""
    user_plant = await user_plant_manager.get_or_404(session, id=id)
    await user_plant_manager.delete(session, user_plant)
    return Response(status_code=204)


# @r.post(
#     "/detect-disease",
#     responses={**to_openapi(UnauthorizedResponse)},
# )
# async def detect(
#     request: Request,
#     session: GetSession,
#     user: authenticated,
#     photo: UploadFile   
# ):
    
#     predict = request.app.state.disease_pipe(photo)
#     return {"ok": predict}
