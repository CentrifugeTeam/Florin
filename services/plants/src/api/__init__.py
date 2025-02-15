from fastapi import APIRouter
from . import welcome

r = APIRouter()
r.include_router(welcome.r)