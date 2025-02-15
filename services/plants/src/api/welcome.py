from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession


r = APIRouter()


@r.get("/")
async def read_root():
  return {"message": "Hello, FastAPI with Poetry and Uvicorn!"}