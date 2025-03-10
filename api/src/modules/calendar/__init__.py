from ...deps import GetSession
from fastapi_libkit.responses import not_found_response
from datetime import date
from sqlalchemy.orm import joinedload
from uuid import UUID
from fastapi import APIRouter, Query, Body, Response, Depends, HTTPException
from ...responses import to_openapi
from typing import Annotated
from .manager import calendar_manager, calendar_event_manager
from .schema import CalendarEventRead
from ..auth.authenticator import authenticator, authenticated
from ...db import CalendarEvent, User

r = APIRouter(prefix="/calendar", tags=["Calendar"])


@r.get("/events", response_model=list[CalendarEventRead])
async def calendar(
    session: GetSession,
    start_date: date,
    end_date: date,
    user: authenticated,
):
    """Get all calendar events for a user between two dates"""

    return await calendar_event_manager.get_events(session, start_date, end_date, user)


@r.get(
    "/events/{id}", response_model=CalendarEventRead, responses={**not_found_response}
)
async def event(session: GetSession, id: UUID, user: User = Depends(authenticator())):
    """Get a calendar event by id"""
    return await calendar_event_manager.get_or_404(
        session, id=id, options=[joinedload(CalendarEvent.user_plant)]
    )


EventAlreadyCompletedResponse = HTTPException(
    status_code=400, detail="Event is already completed"
)


@r.post(
    "/events/{id}/complete",
    response_model=CalendarEventRead,
    responses={**not_found_response, **
               to_openapi(EventAlreadyCompletedResponse)},
)
async def event(session: GetSession, id: UUID, user: User = Depends(authenticator())):
    """Complete event"""
    event: Event = await calendar_event_manager.get_or_404(
        session, id=id, options=[joinedload(CalendarEvent.user_plant)]
    )
    if event.is_completed == True:
        raise EventAlreadyCompletedResponse
    event.is_completed = True
    session.add(event)
    await session.commit()
    return event
