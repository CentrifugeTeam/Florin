from fastapi import APIRouter, Depends, status, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select, delete
from .adapters.token import token_adapter
from .db import User, Token
from ...deps import GetSession
from .authenticator import authenticator
from .manager import user_manager, to_openapi, CouldUploadFileHTTPException
from .scheme import PermissionTokenRead, UserCreate, UserRead
from typing import Annotated
from fastapi_libkit.responses import auth_responses


r = APIRouter(prefix='/users', tags=['Users'])


@r.post('/signup', response_model=UserRead, responses={**to_openapi(CouldUploadFileHTTPException)})
async def signup(
        session: GetSession,
        user: Annotated[UserCreate, Form()]
                 ):
    return await user_manager.create_user(session, user)


@r.post('/login', response_model=PermissionTokenRead, responses={400: {'detail': 'Bad Request'}})
async def login(
        session: GetSession,
        credentials: OAuth2PasswordRequestForm = Depends(),

):
    stmt = select(User).where((credentials.username == User.email) & (User.type == 'password'))
    user = (await session.exec(stmt)).one_or_none()
    if not user:
        # Run the hasher to mitigate timing attack
        # Inspired from Django: https://code.djangoproject.com/ticket/20760
        user_manager.password_helper.hash(credentials.password)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    verified = user_manager.password_helper.verify(
        credentials.password, user.password
    )
    if not verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    token = token_adapter.generate_pair_of_tokens(user.id)

    return PermissionTokenRead(access_token=token)


@r.post('/logout', status_code=status.HTTP_204_NO_CONTENT,
        responses={**auth_responses})
async def logout(
        *,
        user: UserRead = Depends(authenticator()),
        token: Annotated[str, Depends(authenticator.security)],
        session: GetSession
):
    #TODO: delete session from jwt token
    return

