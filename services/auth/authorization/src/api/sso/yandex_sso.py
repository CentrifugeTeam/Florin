import os
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, Request
import logging
from fastapi_sso.sso.yandex import YandexSSO
from fastapi import APIRouter, Depends, status
from ...deps import get_session
from ...managers.users import user_manager
from sqlmodel.ext.asyncio.session import AsyncSession

r = APIRouter(prefix="/yandex")
load_dotenv()

CLIENT_ID = os.getenv("YANDEX_CLIENT_ID")
CLIENT_SECRET = os.getenv("YANDEX_CLIENT_SECRET")
DOMAIN = os.getenv("DOMAIN")

app = FastAPI()

sso = YandexSSO(
  client_id=CLIENT_ID,
  client_secret=CLIENT_SECRET,
  redirect_uri="https://auth.hackcentrifuge.ru/sso/yandex/callback", # DOMAIN + /sso/yandex/callback
  allow_insecure_http=True,
)


@r.get("/login")
async def auth_init():
  async with sso:
    return await sso.get_login_redirect()


@r.get("/callback", description="Callback после входа в Yandex", responses={
  status.HTTP_400_BAD_REQUEST: {"description": "QAUTH2 error"}
})
async def auth_callback(request: Request,
                        session: AsyncSession = Depends(get_session),):
  async with sso:
    user = await sso.verify_and_process(request)

  user_data = user.__dict__
  user_db = await user_manager.create_or_get_user(session, user_data)
  return user_db
