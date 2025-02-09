from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.base import SecurityBase
from fastapi.security.http import get_authorization_scheme_param
from sqlalchemy.ext.asyncio import AsyncSession
from .deps import get_session
from .managers.token import token_manager


class Security(HTTPBearer):
    async def __call__(
            self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        authorization = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            raise HTTPException()
        if scheme.lower() != "bearer":
            raise HTTPException()
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


class AuthBackend:

    def __init__(self, security: SecurityBase):
        self.security = security

    def authenticate(self, verified: bool = False, superuser: bool = False):
        security = self.security

        async def wrapped(
                cred: Annotated[HTTPAuthorizationCredentials, Depends(security)],
                session: AsyncSession = Depends(get_session)
        ):
            user = await token_manager.authenticate(cred.credentials, session)
            exc = UnauthorizedException
            if user:
                exc = ForbidException
                if (
                        verified and not user.is_verified or superuser and not user.is_superuser
                ):
                    user = None

            if not user:
                raise exc

            return user

        return wrapped




auth_backend = AuthBackend(security=Security())
