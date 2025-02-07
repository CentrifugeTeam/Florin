from sqlmodel import Relationship

from ..schemas.profiles import ProfileCreate
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .tokens import PermissionToken, ForgotPasswordToken

class Profile(ProfileCreate):
    __tablename__ = 'profiles'
    permission_tokens: list['PermissionToken'] = Relationship(back_populates='profile')
    forgot_password_tokens: list['ForgotPasswordToken'] = Relationship(back_populates='profile')