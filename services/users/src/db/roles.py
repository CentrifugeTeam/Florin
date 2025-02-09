from ..schemas.roles import RoleRead
from ..schemas.mixins import UUIDMixin


class Role(UUIDMixin, RoleRead, table=True):
    __tablename__ = 'roles'
