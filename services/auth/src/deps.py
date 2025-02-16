from typing import Annotated
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from .conf import session_maker

async def get_session():
    async with session_maker() as session:
        yield session








GetSession = Annotated[AsyncSession, Depends(get_session)]