from fastapi_sqlalchemy_toolkit import ModelManager
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select
from ...db.plants import Plant, UserPlants


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
        super().__init__(UserPlants)

    async def paginated_list(
        self, session: AsyncSession
    ):
        return await session.exec(select(self.model).options(joinedload(UserPlants.plant)))


plant_manager = PlantManager()

user_plant_manager = UserPlantManager()
