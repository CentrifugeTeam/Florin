from ...deps import GetSession
from datetime import date
from sqlalchemy.orm import joinedload
from uuid import UUID
from fastapi import APIRouter, Query, Body, Response, Depends
from typing import Annotated
from .manager import calendar_manger
from .schema import CalendarEvent
from ..auth.authenticator import authenticator
from ...db import Note, Plant, UserPlant, User

r = APIRouter(prefix='/calendar', tags=['Calendar'])


@r.get("", response_model=list[CalendarEvent])
async def calendar(start_date: date,
                   end_date: date,
                   user: User = Depends(authenticator(options=joinedload(User.user_plants)
                                                      .joinedload(UserPlant.plant).joinedload(Plant.cron_schedules)))):
    """
    Для корректной работы endpoint'а нужно отправлять start_date как начало месяца и end_date как конец месяца
    """

    return calendar_manger.get_new_events(start_date, end_date, user)
