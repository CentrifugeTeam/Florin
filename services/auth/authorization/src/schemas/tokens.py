from sqlmodel import SQLModel




class PermissionTokenRead(SQLModel):
    token: str
