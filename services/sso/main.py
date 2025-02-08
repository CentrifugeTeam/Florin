import uvicorn
from fastapi import FastAPI
from src import api

app = FastAPI()
app.include_router(api)


if __name__ == '__main__':
  uvicorn.run('__main__:app', host='0.0.0.0', port=8000, reload=True)