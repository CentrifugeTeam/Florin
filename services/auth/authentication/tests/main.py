from unittest.mock import MagicMock
from pathlib import Path
from dotenv import load_dotenv
import sys
path = str((Path(__file__).parent.parent / 'authentication').absolute())
load_dotenv()
sys.path.append(path)

from authentication.main import handler


def test_handler():
    event = {}
    context = {}

    event['body'] = '{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3NGZkMGExYi00NjdlLTQwMGQtOWZiZC01NDExZWU2MmNhODYiLCJleHAiOjE3Mzk4ODM4Mzh9._tviqVJe-dz4QVdN4Et7WXNpi1RyRHoF7v7FpbzKpOg"}'
    handler(event, context)