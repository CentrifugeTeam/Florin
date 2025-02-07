import uvicorn
from fastapi import FastAPI
from src.api import api

app = FastAPI()
app.include_router(api)

# TODO: наверное нужно разбить на такие сервисы
#  - сервис пользователей с данными про пользователей (статистика, поиск пользователя)
#  - сервис авторизации (логин по SSO, логину и паролу, востановление пароля и тд)
#  - сервис аутентификации (валидация токена, для быстрой вызова данной функции другими сервисами)

if __name__ == '__main__':
    uvicorn.run('__main__:app', host='0.0.0.0', port=8000, reload=True)