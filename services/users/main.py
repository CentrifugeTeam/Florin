import uvicorn
from fastapi import FastAPI
from sqlalchemy import text

from src.conf import *

app = FastAPI()

@app.get("/")
async def hello():
    async with session_maker() as session:
        res = (await session.execute(text("SELECT 1"))).scalar()

    return {"message": f"Hello World {res}"}

# TODO: наверное нужно разбить на такие сервисы
#  - сервис пользователей с данными про пользователей (статистика, поиск пользователя)
#  - сервис авторизации (логин по SSO, логину и паролу, востановление пароля и тд)
#  - сервис аутентификации (валидация токена, для быстрой вызова данной функции другими сервисами)

if __name__ == '__main__':
    uvicorn.run('__main__:app', host='0.0.0.0', port=8000, reload=True)