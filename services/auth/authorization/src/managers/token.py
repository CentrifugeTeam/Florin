from sqlmodel import col

from ..conf import settings
from datetime import datetime, timezone, timedelta
from sqlalchemy import delete, select
from uuid import UUID
import jwt
from sqlmodel.ext.asyncio.session import AsyncSession

from ..db.profile import Account, Token
from ..exceptions import JwtAuthError


class TokenManager:
    def __init__(
            self,
            key: str,
            access_token_lifetime: timedelta,
            algorithm: str = "HS256",

    ):
        self.algorithm = algorithm
        self.key = key
        self.access_token_lifetime = access_token_lifetime


    def generate_pair_of_tokens(self, user_id: UUID):
        payload = {"sub": str(user_id)}
        payload['exp'] = datetime.now(timezone.utc) + self.access_token_lifetime
        token = jwt.encode(payload, self.key, algorithm=self.algorithm)
        return token

    async def authenticate(
            self, access_token: str, session: AsyncSession
    ):
        res = self.decode_token(access_token)

        stmt = select(Account).join(Token, Token.id == Account.token_id).where(col(Token.token) == access_token).where(
            Account.profile_id == res['sub'])
        return await session.exec(stmt)

    def decode_token(self, token: str):
        """
        :param token:
        :return:
        """
        try:
            payload = jwt.decode(
                token, self.key, algorithms=[self.algorithm]
            )
            payload['sub'] = UUID(payload['sub'])

        except (jwt.PyJWTError, ValueError, jwt.ExpiredSignatureError):
            raise JwtAuthError
        return payload

    async def logout(self, session: AsyncSession, user_id: UUID, access_token: str) -> None:
        res = self.decode_token(access_token)
        if res['sub'] != user_id:
            raise JwtAuthError

        stmt = delete(Account).where(col(Account.token) == access_token).where(
            Account.profile_id == res['sub'])
        res = await session.exec(stmt)
        await session.commit()

    async def login(self, session: AsyncSession, user_id: UUID):
        access_token = self.generate_pair_of_tokens(user_id)
        user_token = Account(profile_id=user_id, token=access_token)
        session.add(user_token)
        await session.commit()
        return user_token


token_manager = TokenManager(settings.JWT_PRIVATE_KEY, access_token_lifetime=timedelta(days=2)                             )
