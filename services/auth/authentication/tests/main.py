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

    event['body'] = '{"token":"hello"}'
    handler(event, context)