from fastapi import APIRouter
from .accounts import r

api = APIRouter()
api.include_router(r)
