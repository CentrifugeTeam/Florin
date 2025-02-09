import os
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, Request
import logging
from fastapi_sso.sso.yandex import YandexSSO
from fastapi import APIRouter

r = APIRouter(prefix="/yandex")
load_dotenv()

CLIENT_ID = os.getenv("YANDEX_CLIENT_ID")
CLIENT_SECRET = os.getenv("YANDEX_CLIENT_SECRET")
DOMAIN = os.getenv("DOMAIN")

app = FastAPI()

sso = YandexSSO(
  client_id=CLIENT_ID,
  client_secret=CLIENT_SECRET,
  redirect_uri="http://127.0.0.1:8000/sso/yandex/callback", # DOMAIN + /sso/yandex/callback
  allow_insecure_http=True,
)


@r.get("/login")
async def auth_init():
  async with sso:
    return await sso.get_login_redirect()


@r.get("/callback")
async def auth_callback(request: Request):
  async with sso:
    user = await sso.verify_and_process(request)
    return user
