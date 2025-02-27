from typing import Annotated
from fastapi import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlmodel import select, delete
from sqlalchemy.exc import MultipleResultsFound
from ...deps import GetSession
from ...db import User, Token
from .adapters.token import token_adapter, JwtAuthError
from fastapi import Depends

ForbidResponse = HTTPException(status_code=403, detail="Forbidden")
UnauthorizedResponse = HTTPException(
    status_code=401, detail="Unauthorized")


class Authenticator:

    def __init__(self, security: OAuth2PasswordBearer):
        self.security = security

    def __call__(self, is_verified: bool = False, superuser: bool = False):
        security = self.security

        async def wrapped(
                token: Annotated[str, Depends(security)],
                session: GetSession
        ):

            exc = UnauthorizedResponse
            try:
                jwt = token_adapter.decode_token(token)
            except JwtAuthError:
                raise exc

            stmt = select(User).join(Token, Token.user_id == User.id).where(
                (Token.token == token) & (Token.user_id == jwt['sub']))
            try:
                result = await session.exec(stmt)
                user = result.one_or_none()
            except MultipleResultsFound:
                # several users use the same token then clear it all
                tokens = await session.exec(select(Token).where(Token.token == token))
                for token in tokens:
                    await session.delete(token)
                await session.commit()
                user = None

            if user:
                exc = ForbidResponse
                if (
                        is_verified and not user.is_verified or superuser and not user.is_superuser
                ):
                    user = None

            if not user:
                raise exc

            return user

        return wrapped


authenticator = Authenticator(
    security=OAuth2PasswordBearer(tokenUrl='api/auth/login'))


authenticate = Annotated[User, Depends(authenticator())]
