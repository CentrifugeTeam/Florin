from fastapi import APIRouter
from . import users, sso

api = APIRouter()
api.include_router(users.r)
api.include_router(sso.r)
