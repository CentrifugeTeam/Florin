from typing import Iterable, Any
from fastapi import UploadFile, HTTPException
from fastapi_sqlalchemy_toolkit.model_manager import CreateSchemaT, ModelT, ModelManager
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlmodel import col
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status
from shared.storage.db.models import User, Role
from ..schemas.users import UserCredentials
from ..exceptions import UserAlreadyVerifiedException
from secrets import token_urlsafe
from ..db import User, ForgotPasswordToken
from .files import file_manager


class UsersManager(ModelManager):

    def __init__(self) -> None:
        super().__init__(User)
        self.password_helper = PasswordHelper()

    async def forgot_password(self, session: AsyncSession, user: User):
        token = token_urlsafe(32)
        obj = ForgotPasswordToken(user_id=user.id, token=token)
        session.add(obj)
        await session.commit()
        return token

    async def verify(self, session: AsyncSession, token: str):
        stmt = select(ForgotPasswordToken).where(col(ForgotPasswordToken.token) == token).options(joinedload(ForgotPasswordToken.user))
        token = await session.exec(stmt)
        if not token:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Token not found')
        user = token.user
        if user.is_verified:
            raise UserAlreadyVerifiedException

        user.is_verified = True
        session.add(user)
        await session.commit()
        return user


    async def reset_password(self, session: AsyncSession, token: str, new_password: str):

        stmt = select(ForgotPasswordToken).where(col(ForgotPasswordToken.token) == token).options(
            joinedload(ForgotPasswordToken.user))
        token = await session.exec(stmt)
        if not token:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Token not found')
        user = token.user

        user.password = self.password_helper.hash(new_password)
        session.add(user)
        await session.commit()
        return user


    async def create_user(
            self,
            session: AsyncSession,
            in_obj: CreateSchemaT | None = None,
            file: UploadFile | None = None,
            *,
            commit: bool = True,
            refresh_attribute_names: Iterable[str] | None = None,
            role_name: str = 'usual',
            **attrs: Any,
    ) -> ModelT:

        in_obj.password = self.password_helper.hash(in_obj.password)
        create_data = in_obj.model_dump()
        create_data.update(attrs)

        # Добавляем дефолтные значения полей для валидации уникальности
        for field, default in self.defaults.items():
            if field not in create_data:
                create_data[field] = default

        await self.run_db_validation(session, in_obj=create_data)
        if file is not None:
            try:
                photo_url = await file_manager.save_file(file)
                create_data['photo_url'] = photo_url
            except Exception:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Could not upload file')
        else:
            create_data['photo_url'] = None

        db_obj = self.model(**create_data)
        stmt = select(Role).where(Role.name == role_name)
        role = await session.scalar(stmt)
        if not role:
            role = Role(name=role_name)
        db_obj.roles.append(role)
        session.add(db_obj)

        await self.save(session, commit=commit)

        await session.refresh(db_obj, attribute_names=refresh_attribute_names)
        return db_obj


    async def authenticate(self, session: AsyncSession, credentials: UserCredentials):
        stmt = select(User).where(credentials.login == User.username) # type: ignore
        user = (await session.execute(stmt)).scalar()
        if not user:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            self.password_helper.hash(credentials.password)
            return None
        if user.password is None:
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.password
        )
        if not verified:
            return None
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            user.password = updated_password_hash
            session.add(user)
            await session.commit()

        return user


user_manager = UsersManager()