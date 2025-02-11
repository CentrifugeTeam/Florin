from typing import Annotated
from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .db import User, Token
from .deps import get_session
from .adapters.token import token_adapter
from .exceptions import JwtAuthError, UnauthorizedException, ForbidException


class AuthBackend:

    def __init__(self, security: OAuth2PasswordBearer):
        self.security = security

    def authenticate(self, is_verified: bool = False, superuser: bool = False):
        security = self.security

        async def wrapped(
                token: Annotated[str, Depends(security)],
                session: AsyncSession = Depends(get_session)
        ):

            exc = UnauthorizedException
            try:
                jwt = token_adapter.decode_token(token)
            except JwtAuthError:
                raise exc

            stmt = select(User).join(Token, Token.user_id == User.id).where((Token.token == token) & (Token.user_id == jwt['sub']))
            user = (await session.exec(stmt)).one_or_none()

            if user:
                exc = ForbidException
                if (
                        is_verified and not user.is_verified or superuser and not user.is_superuser
                ):
                    user = None

            if not user:
                raise exc

            return user

        return wrapped




auth_backend = AuthBackend(security=OAuth2PasswordBearer(tokenUrl='login'))
