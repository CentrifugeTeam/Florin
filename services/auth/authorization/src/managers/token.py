from fastapi_sqlalchemy_toolkit import ModelManager

from ..db import Token


class TokenManager(ModelManager):
    def __init__(self):
        super().__init__(Token)



token_manager = TokenManager()