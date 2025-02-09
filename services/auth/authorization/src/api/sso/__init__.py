from fastapi import APIRouter
from . import google_sso, yandex_sso

r = APIRouter(prefix="/sso")
r.include_router(google_sso.r)
r.include_router(yandex_sso.r)