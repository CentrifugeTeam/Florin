from fastapi import APIRouter
from . import google_sso

r = APIRouter(prefix="/sso")
r.include_router(google_sso.r)
