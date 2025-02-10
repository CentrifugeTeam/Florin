from .base import BaseManager
from ..conf import settings
from ..db import UserToken, User
from datetime import datetime, timezone, timedelta
from sqlalchemy import delete, select
from uuid import UUID
import jwt
from sqlmodel.ext.asyncio.session import AsyncSession
from ..responses import MissingTokenOrInactiveUserException, UnauthorizedInvalidDataException


class TokenManager(BaseManager):
    def __init__(
            self,
            key: str,
            refresh_token_lifetime: timedelta,
            access_token_lifetime: timedelta,
            algorithm: str = "HS256",

    ):
        super().__init__(UserToken)
        self.algorithm = algorithm
        self.key = key
        self.access_token_lifetime = access_token_lifetime
        self.refresh_token_lifetime = refresh_token_lifetime


    def generate_pair_of_tokens(self, user_id: UUID):
        payload = {"sub": str(user_id)}
        payload['exp'] = datetime.now(timezone.utc) + self.access_token_lifetime
        access_token = jwt.encode(payload, self.key, algorithm=self.algorithm)
        payload['exp'] = datetime.now(timezone.utc) + self.refresh_token_lifetime
        refresh_token = jwt.encode(payload, self.key, algorithm=self.algorithm)
        return access_token, refresh_token

    async def authenticate(
            self, access_token: str, session: AsyncSession
    ):
        res = self.decode_token(access_token)

        stmt = select(User).join(UserToken).where(UserToken.access_token == access_token).where(
            UserToken.user_id == res['sub'])
        return (await session.exec(stmt)).scalar()

    def decode_token(self, token: str):
        """
        :raises MissingTokenOrInactiveUserException
        :param token:
        :return:
        """
        try:
            payload = jwt.decode(
                token, self.key, algorithms=[self.algorithm]
            )
            payload['sub'] = UUID(payload['sub'])

        except (jwt.PyJWTError, ValueError, jwt.ExpiredSignatureError):
            raise MissingTokenOrInactiveUserException
        return payload


token_manager = TokenManager(settings.JWT_PRIVATE_KEY, access_token_lifetime=timedelta(days=2),
                             )
