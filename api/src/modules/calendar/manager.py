from fastapi_sqlalchemy_toolkit import ModelManager
from datetime import date, datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select
from sqlalchemy import asc
from croniter import croniter, croniter_range
from .schema import CalendarEventRead
from ..plants.schema import PlantRead
from ...db import CronPlantCalendarScheduler, User, CalendarEvent, Plant, UserPlant


class CalendarManager(ModelManager):
    def __init__(self):
        super().__init__(CronPlantCalendarScheduler)

    def get_new_datetime_in_interval(
        self,
        start_date: date,
        end_date: date,
        cron_schedule: CronPlantCalendarScheduler,
    ):
        for event_datetime in croniter_range(
            start_date, end_date, cron_schedule.cron_expression, ret_type=datetime
        ):
            yield event_datetime


class CalendarEventManager(ModelManager):
    async def get_events(
        self,
        session: AsyncSession,
        start_date: date,
        end_date: date,
        user: User,
    ):
        stmt = (
            select(UserPlant)
            .options(joinedload(UserPlant.plant).subqueryload(Plant.cron_schedules))
            .where(UserPlant.user_id == user.id)
        )
        user_plants = await session.exec(stmt)
        for user_plant in user_plants:
            plant = user_plant.plant
            # get default schedule
            schedule = plant.cron_schedules[0]
            for new_datetime in calendar_manager.get_new_datetime_in_interval(
                start_date, end_date, schedule
            ):
                stmt = (
                    select(CalendarEvent)
                    .where(CalendarEvent.user_plant_id == user_plant.id)
                    .where(CalendarEvent.do_on == new_datetime)
                )
                if (await session.exec(stmt)).first():
                    continue

                event = CalendarEvent(
                    is_completed=False,
                    do_on=new_datetime,
                    header="Полив растения",
                    content=f"Успей полить растение {plant.name or plant.origin_name}",
                    user_plant_id=user_plant.id,
                )
                session.add(event)

        await session.commit()

        stmt = (
            select(CalendarEvent)
            .join(UserPlant, CalendarEvent.user_plant_id == UserPlant.id)
            .join(User, User.id == UserPlant.user_id)
            .where(User.id == user.id)
            .where(CalendarEvent.do_on >= start_date)
            .where(CalendarEvent.do_on <= end_date)
            .order_by(asc(CalendarEvent.do_on))
            .options(joinedload(CalendarEvent.user_plant))
        )

        return await session.exec(stmt)


calendar_event_manager = CalendarEventManager(CalendarEvent)
calendar_manager = CalendarManager()
