from ...deps import GetSession
from fastapi_libkit.responses import ErrorModel, not_found_response, no_content_response
from sqlalchemy.orm import joinedload
from uuid import UUID
from fastapi import APIRouter, Query, Body, Response
from typing import Annotated
from .manager import plant_manager, user_plant_manager
from .schema import PlantRead, PlantCard, NoteRead, UserPlantRead, UserPlantsProfile
from ...shared.responses import to_openapi
from ..auth.authenticator import authenticated, UnauthorizedResponse
from ...db import Note, Plant, UserPlant

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
    session: GetSession,
    id: UUID,
    user: authenticated,
    name: Annotated[str | None, Body(embed=True)] = None,
):
    plant = await plant_manager.get_or_404(session, id=id)
    user_plant = UserPlant(name=name or plant.name, user_id=user.id, plant_id=plant.id)
    session.add(user_plant)
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
