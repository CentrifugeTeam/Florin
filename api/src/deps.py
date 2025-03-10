from redis.asyncio import Redis
from typing import Annotated
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from .conf import session_maker, connection_pool


async def get_session():
    async with session_maker() as session:
        yield session


async def get_redis():
    r = Redis(connection_pool=connection_pool)
    async with r:
        yield r


GetSession = Annotated[AsyncSession, Depends(get_session)]
GetRedis = Annotated[Redis, Depends(get_redis)]
