from fastapi_sqlalchemy_toolkit import ModelManager
from datetime import date, datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select
from croniter import croniter, croniter_range
from .schema import CalendarEvent
from ..plants.schema import PlantRead
from ...db import CronPlantCalendarScheduler, User


class CalendarManager(ModelManager):
    def __init__(self):
        super().__init__(CronPlantCalendarScheduler)

    def get_new_events(self, start_date: date, end_date: date, user: User):
        events = []
        for user_plant in user.user_plants:
            # правильнее было бы брать планирование в соответствии с сезоном
            cron_schedule = user_plant.plant.cron_schedules[0]
            for event_datetime in croniter_range(start_date, end_date, cron_schedule.cron_expression, ret_type=datetime):
                events.append(
                    CalendarEvent(
                        datetime=event_datetime, plant=PlantRead.model_validate(user_plant.plant))
                )

        return events


calendar_manger = CalendarManager()
