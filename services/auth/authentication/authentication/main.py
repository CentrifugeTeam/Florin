import json
from uuid import UUID

import jwt
from src.conf import driver, settings
from ydb import QuerySessionPool


class HttpException(Exception):
  def __init__(self, status_code, message: dict | str):
    self.message = message
    self.status_code = status_code



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


def fetch(event: dict, context: dict):
  try:
    token = json.loads(event['body'])['token']
  except:
    raise HttpException(status_code=400, message='Bad Request')

  db = decode_token(token)
  return db[0].rows[0]


def create(event: dict, context: dict):
  pass


def handler(event: dict, context: dict):
  route_path = event['path']
  try:
    if route_path == '/fetch':
      response = fetch(event, context)
    elif route_path == '/create':
      response = create(event, context)
    else:
      return {
        'statusCode': 404,
        'body': 'Not found',
        'isBase64Encoded': False,
      }
  except HttpException as exc:
    return {
      'statusCode': exc.status_code,
      'body': exc.message,
      'isBase64Encoded': False,
    }
  except Exception as exc:
    return {
      'statusCode': 500,
      'body': "Server Error",
      'isBase64Encoded': False,
    }

  return {
    'statusCode': 200,
    'body': response,
    'isBase64Encoded': False,
  }
