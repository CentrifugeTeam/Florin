from fastapi import FastAPI
import uvicorn
from src.modules import users, sso


app = FastAPI(root_path='/api')
app.include_router(users.r)
app.include_router(sso.r)


if __name__ == '__main__':

  uvicorn.run('__main__:app', host='0.0.0.0', port=8000, reload=True)