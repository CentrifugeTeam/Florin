from pydantic import BaseModel

class PermissionTokenRead(BaseModel):
    access_token: str
    token_type: str = 'bearer'
