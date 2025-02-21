from typing import Annotated
from fastapi import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlmodel import select
from ...deps import GetSession
from .db import User, Token
from .adapters.token import token_adapter, JwtAuthError
from fastapi import Depends

class Authenticator:

    ForbidException = HTTPException(status_code=403, detail="Forbidden")
    UnauthorizedException = HTTPException(status_code=401, detail="Unauthorized")

    def __init__(self, security: OAuth2PasswordBearer):
        self.security = security

    def __call__(self, is_verified: bool = False, superuser: bool = False):
        security = self.security

        async def wrapped(
                token: Annotated[str, Depends(security)],
                session: GetSession
        ):

            exc = self.UnauthorizedException
            try:
                jwt = token_adapter.decode_token(token)
            except JwtAuthError:
                raise exc

            stmt = select(User).join(Token, Token.user_id == User.id).where((Token.token == token) & (Token.user_id == jwt['sub']))
            user = (await session.exec(stmt)).one_or_none()

            if user:
                exc = self.ForbidException
                if (
                        is_verified and not user.is_verified or superuser and not user.is_superuser
                ):
                    user = None

            if not user:
                raise exc

            return user

        return wrapped


authenticator = Authenticator(security=OAuth2PasswordBearer(tokenUrl='login'))