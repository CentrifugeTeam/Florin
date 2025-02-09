from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import HTTPAuthorizationCredentials
from logging import getLogger
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from ..db import Account
from ..deps import get_session
from ..auth_backend import auth_backend
from ..managers.token import token_manager
from ..managers.users import user_manager
from ..schemas.tokens import PermissionTokenRead
from ..schemas.profiles import UserCreate, ProfileRead
from fastapi_libkit.responses import auth_responses, missing_token_or_inactive_user_response
from fastapi_libkit.schemas import as_form


r = APIRouter()


@r.post('/signup', response_model=ProfileRead)
async def signup(user: UserCreate = Depends(as_form(UserCreate)),
                 session: AsyncSession = Depends(get_session)):
    return await user_manager.create_user(session, user)


@r.post('/login', response_model=PermissionTokenRead, responses={**missing_token_or_inactive_user_response, **auth_responses})
async def login(
        credentials: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session)
):
    stmt = select(Account).where(Account.login == credentials.username).where(Account.password == credentials.password).where(Account.type == 'password')
    account = await session.exec(stmt)
    if not account:
        raise Exception

    token = await token_manager.login(session, account.profile_id)
    return PermissionTokenRead(access_token=token.access_token, refresh_token=token.refresh_token)


@r.post('/logout', status_code=status.HTTP_204_NO_CONTENT,
        responses={**auth_responses})
async def logout(
        *,
        profile: ProfileRead = Depends(auth_backend.authenticate()),
        cred: Annotated[HTTPAuthorizationCredentials, Depends(auth_backend.security)],
        session: AsyncSession = Depends(get_session)
):
    return await token_manager.logout(session, profile.id, cred.credentials)

