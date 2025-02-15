import json
from uuid import UUID

def decode_token(token: str):
  pass


def encode_token(user_id: UUID):
  pass


def handler(event: dict, context: dict):

  token = json.loads(event['body'])['token']
  decode_token(token)


  return {
    'body': {**event, **context},
    'isBase64Encoded': False,
  }
