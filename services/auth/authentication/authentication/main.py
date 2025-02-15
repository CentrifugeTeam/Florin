from uuid import UUID


def decode_token():
  pass


def encode_token(user_id: UUID):
  pass


def handler(event: dict, context: dict):
  return {
    'body': {**event, **context},
    'isBase64Encoded': False,
  }
