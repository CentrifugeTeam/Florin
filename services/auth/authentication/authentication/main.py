import json
from uuid import UUID

import jwt
from src.conf import driver, settings
from ydb import QuerySessionPool


def decode_token(token: str):
  try:
    payload = jwt.decode(token, settings.JWT_PRIVATE_KEY, algorithms=['HS256'])
  except:
    raise jwt.InvalidTokenError
  with QuerySessionPool(driver) as session:
    user = session.execute_with_retries(
      """
      DECLARE $uuid AS TEXT;
      SELECT * FROM users
      WHERE users.id = $uuid
      """,
      {
        '$uuid': UUID(payload['sub']).hex # change creating jwt token from UUID to hex

      }

    )
  return user




def handler(event: dict, context: dict):
  token = json.loads(event['body'])['token']
  user = decode_token(token)

  return {
    'body': user,
    'isBase64Encoded': False,
  }
