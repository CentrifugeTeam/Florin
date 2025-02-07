from sqlmodel import SQLModel
from .mixins import UUIDMixin
from fastapi_sqlalchemy_toolkit import make_partial_model



class RoleBase(SQLModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleRead(UUIDMixin, RoleBase):
    pass





RoleUpdate = make_partial_model(RoleCreate)
