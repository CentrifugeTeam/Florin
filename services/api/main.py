from fastapi import FastAPI
import uvicorn
from src.modules import users, sso


app = FastAPI(root_path='/api')
app.include_router(users.r)
app.include_router(sso.r)

