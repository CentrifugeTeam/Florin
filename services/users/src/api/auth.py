from typing import Annotated

from fastapi import APIRouter, Depends, Body, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import HTTPAuthorizationCredentials
from logging import getLogger
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.authorization.src.db import User
from ..deps import get_session
from ..backend import auth_backend
from ..managers import user_manager
from ..schemas.tokens import PermissionTokenRead
from ..schemas.profiles import ProfileCreate, ProfileRead
from fastapi_libkit.responses import auth_responses
from fastapi_libkit.schemas import as_form

logger = getLogger(__name__)

r = APIRouter()


@r.post('/register', response_model=ProfileRead)
async def user(user: ProfileRead = Depends(as_form(ProfileCreate)),
               session: AsyncSession = Depends(get_session)):
    return await user_manager.create_user(session, user)


@r.post('/login', response_model=PermissionTokenRead, responses={**incorrect_credentials_response, **auth_responses})
async def login(
        credentials: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session)
):
    try:
        user = await user_manager.login(session, credentials)
    except UserNotFoundException:
        raise IncorrectCredentialsException
    return await auth_backend.login(session, user)


@r.post('/logout', status_code=status.HTTP_204_NO_CONTENT,
        responses={**auth_responses})
async def logout(
        *,
        user: User = Depends(auth_backend.authenticator()),
        cred: Annotated[OAuth2PasswordRequestForm, Depends(auth_backend.security)],
        session: AsyncSession = Depends(get_session)
):
    await auth_backend.logout(session, user, cred)
    return


@r.post(
    "/refresh-token",
    response_model=PermissionTokenRead
)
async def refresh(refresh_token: str = Body(embed=True),
                  session: AsyncSession = Depends(get_session)
                  ):
    return await auth_backend.refresh_token(session, refresh_token)
