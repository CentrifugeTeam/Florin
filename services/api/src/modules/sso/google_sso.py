import os
from dotenv import load_dotenv
from fastapi import Request
from fastapi_sso.sso.google import GoogleSSO
from fastapi import APIRouter, Depends, status
from ...deps import get_session
from ..users.manager import user_manager
from sqlmodel.ext.asyncio.session import AsyncSession


r = APIRouter(prefix="/google")
load_dotenv()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
DOMAIN = os.getenv("DOMAIN")

sso = GoogleSSO(
  client_id=CLIENT_ID,
  client_secret=CLIENT_SECRET,
  redirect_uri=f"{DOMAIN}/sso/google/callback", # DOMAIN + /sso/google/callback
  allow_insecure_http=True,
)


@r.get("/login")
async def auth_init():
  async with sso:
    return await sso.get_login_redirect(params={"prompt": "consent", "access_type": "offline"})


@r.get("/callback", description="Callback после входа в Google", responses={
  status.HTTP_400_BAD_REQUEST: {"description": "QAUTH2 error"}
})
async def auth_callback(request: Request,
                        session: AsyncSession = Depends(get_session),):
  async with sso:
    user = await sso.verify_and_process(request)

  user_data = user.__dict__
  user_db = await user_manager.create_or_get_user(session, user_data)
  return user_db
