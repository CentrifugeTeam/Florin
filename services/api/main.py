from fastapi import FastAPI
from src.modules import users, sso


app = FastAPI(root_path='/api')
app.include_router(users.r)
app.include_router(sso.r)

