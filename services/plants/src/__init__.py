from fastapi import APIRouter
from .api import r

api = APIRouter()
api.include_router(r)
