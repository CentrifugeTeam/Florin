from uuid import UUID


def decode_token():
  pass


def encode_token(user_id: UUID):
  pass


def handler(request: dict, context: dict):
  return {
    'body': {**request, **context},
    'isBase64Encoded': False,
  }
