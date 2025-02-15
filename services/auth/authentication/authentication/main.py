import json
from src.db import User
from src.conf import session_maker
from sqlmodel import select

def decode_token(token: str):
  pass


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
