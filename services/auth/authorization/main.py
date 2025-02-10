from fastapi import FastAPI

from mangum.handlers.api_gateway import HTTPGateway
from mangum import Mangum
from src import api

app = FastAPI()
app.include_router(api)

handler = Mangum(app, custom_handlers=[HTTPGateway])

if __name__ == '__main__':
  import uvicorn
  uvicorn.run('__main__:app', host='0.0.0.0', port=8000, reload=True)