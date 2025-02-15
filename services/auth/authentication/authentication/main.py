import json

from sqlmodel import select
from src.conf import session_maker
from src.db import Token, User


def decode_token(token: str):
  stmt = select(Token).where(Token.token == token)
  with session_maker() as session:
    # TODO: test it
    result = session.exec(stmt)
    print(result)


def handler(event: dict, context: dict):
  stmt = select(User.id)
  with session_maker() as session:
    result = session.exec(stmt)
    print(result)
  token = json.loads(event['body'])['token']
  decode_token(token)


  return {
    'body': {'result': result},
    'isBase64Encoded': False,
  }
