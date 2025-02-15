from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession
from ..adapters.token import token_adapter
from ..db import User, Token
from ..deps import get_session
from ..auth_backend import auth_backend
from ..managers.users import user_manager, CouldUploadFileHTTPException, to_openapi
from ..schemas.tokens import PermissionTokenRead
from ..schemas.users import UserCreate, UserRead
from fastapi_libkit.responses import auth_responses, bad_request_response
from fastapi_libkit.schemas import as_form


r = APIRouter()


@r.post('/signup', response_model=UserRead, responses={**to_openapi(CouldUploadFileHTTPException)})
async def signup(user: UserCreate = Depends(as_form(UserCreate)),
                 session: AsyncSession = Depends(get_session)):
    return await user_manager.create_user(session, user)


@r.post('/login', response_model=PermissionTokenRead, responses={**bad_request_response})
async def login(
        credentials: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session)
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

    token = Token(token=token_adapter.generate_pair_of_tokens(user.id), user_id=user.id)
    session.add(token)
    await session.commit()
    return PermissionTokenRead(access_token=token.token)



@r.post('/logout', status_code=status.HTTP_204_NO_CONTENT,
        responses={**auth_responses})
async def logout(
        *,
        user: UserRead = Depends(auth_backend.authenticate()),
        token: Annotated[str, Depends(auth_backend.security)],
        session: AsyncSession = Depends(get_session)
):
    stmt = delete(Token).where((Token.user_id == user.id) & (Token.token == token))
    await session.exec(stmt)
    return 
    # return await token_manager.logout(session, user.id, cred.credentials)

