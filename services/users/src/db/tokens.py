from uuid import UUID

from .profile import Profile
from ..schemas.tokens import ForgotPasswordTokenCreate, PermissionTokenRead
from ..schemas.mixins import UUIDMixin
from sqlmodel import Field, Relationship


class ForgotPasswordToken(UUIDMixin, ForgotPasswordTokenCreate, table=True):
    __tablename__ = 'forgot_password_tokens'
    profile_id: UUID = Field(foreign_key='profiles.id')
    profile: Profile = Relationship(back_populates='forgot_password_tokens')


class PermissionToken(UUIDMixin, PermissionTokenRead, table=True):
    profile_id: UUID = Field(foreign_key='profiles.id')
    profile: Profile = Relationship(back_populates='permissions_tokens')
