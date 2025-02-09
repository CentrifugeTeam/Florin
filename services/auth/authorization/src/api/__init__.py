from fastapi import APIRouter
from . import sso, auth

r = APIRouter()
r.include_router(sso.r)
r.include_router(auth.r)
