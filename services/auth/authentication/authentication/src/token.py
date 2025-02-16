from .conf import settings
from datetime import datetime, timezone, timedelta
from uuid import UUID
import jwt

class JwtException(Exception):
    pass


class TokenAdapter:
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

    def decode_token(self, token: str) -> dict:
        """
        :raises JwtAuthError
        :param token:
        :return:
        """
        try:
            payload = jwt.decode(
                token, self.key, algorithms=[self.algorithm]
            )
            payload['sub'] = UUID(payload['sub'])

        except (jwt.PyJWTError, ValueError, jwt.ExpiredSignatureError):
            raise JwtException
        return payload

token_adapter = TokenAdapter(settings.JWT_PRIVATE_KEY, access_token_lifetime=timedelta(days=2))
