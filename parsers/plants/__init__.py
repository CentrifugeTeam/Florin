from sqlalchemy.ext.asyncio import AsyncSession
from ..conf import session_maker 
from .plants_service import Plants

async def main():
  async with session_maker() as session:
    plants = Plants(session)
    result = await plants.run()
