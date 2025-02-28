from ...deps import GetSession
from uuid import UUID
from sqlmodel import select, update
from fastapi import APIRouter, Query, Depends, Body
from ..auth.authenticator import authenticator, authenticated
from typing import Annotated
from ...db import User
from ..auth.manager import user_manager
from ..auth.scheme import UserRead

r = APIRouter(prefix='/users', tags=['Users'])


@r.get("", response_model=list[UserRead])
async def users(session: GetSession):
    return await user_manager.list(session)


@r.get("/me", response_model=UserRead)
async def me(
    user: authenticated,
):
    return user


@r.patch("/{id}", response_model=UserRead)
async def users(session: GetSession, id: UUID, username: Annotated[str, Body(embed=True)],
                user: authenticated):
    stmt = update(User).where(User.id == id).values(
        username=username).returning(User)
    updated_user = (await session.exec(stmt)).scalar()
    await session.commit()
    return updated_user
