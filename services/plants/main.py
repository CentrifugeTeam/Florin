from fastapi import FastAPI

from mangum.handlers.api_gateway import HTTPGateway
from mangum import Mangum
from src import api

app = FastAPI(root_path='/auth')
app.include_router(api)

handler = Mangum(app, custom_handlers=[HTTPGateway], api_gateway_base_path='/auth')

if __name__ == '__main__':
  import uvicorn
  uvicorn.run('__main__:app', host='127.0.0.1', port=8000, reload=True)