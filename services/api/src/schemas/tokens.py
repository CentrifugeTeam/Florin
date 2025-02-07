from sqlmodel import SQLModel

class ForgotPasswordTokenCreate(SQLModel):
    token: str


class PermissionTokenRead(SQLModel):
    access_token: str
    refresh_token: str
