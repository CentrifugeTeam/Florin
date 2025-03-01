from fastapi import FastAPI
from src.modules import plants, auth, files, users, calendar, articles, chat


app = FastAPI()
app.include_router(auth.r)
# app.include_router(sso.r)
app.include_router(plants.r)
app.include_router(files.r)
app.include_router(users.r)
app.include_router(calendar.r)
app.include_router(articles.r)
app.include_router(chat.r)
