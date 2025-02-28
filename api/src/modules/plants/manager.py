from fastapi_sqlalchemy_toolkit import ModelManager
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select
from ...db import Plant, UserPlant, User


class PlantManager(ModelManager):
    def __init__(self):
        super().__init__(Plant)

    async def paginated_list(
        self, session: AsyncSession,  page: int, limit: int
    ):
        offset = (page - 1) * limit
        return await session.exec(select(self.model).offset(offset).limit(limit))


class UserPlantManager(ModelManager):
    def __init__(self):
        super().__init__(UserPlant)

    async def paginated_list(
        self, session: AsyncSession, user: User
    ):
        user = (await session.exec(select(User).options(joinedload(User.user_plants).joinedload(UserPlant.plant)).where(User.id == user.id))).unique().one()
        return user.user_plants


plant_manager = PlantManager()

user_plant_manager = UserPlantManager()
