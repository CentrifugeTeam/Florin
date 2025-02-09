from fastapi import APIRouter
from . import user_password, verify

r = APIRouter(prefix="/accounts")
r.include_router(user_password.r)
r.include_router(verify.r)
