from fastapi_sqlalchemy_toolkit import ModelManager
from datetime import date, datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select
from ...db.calendar import CronPlantCalendarScheduler


class CalendarManager(ModelManager):
    def __init__(self):
        super().__init__(CronPlantCalendarScheduler)

    async def get_new_events(self, date: date):
        pass


calendar_manger = CalendarManager()
