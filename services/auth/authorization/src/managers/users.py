from typing import Iterable, Any
from fastapi import UploadFile, HTTPException
from fastapi_sqlalchemy_toolkit.model_manager import ModelT, ModelManager
from sqlmodel.ext.asyncio.session import AsyncSession

from ..schemas.profiles import UserCreate
from ..db import Profile, Account, Token
from starlette import status
from passlib.hash import pbkdf2_sha256
from .files import file_manager
from secrets import token_urlsafe

account_manager = ModelManager(Account)


class UsersManager(ModelManager):

    def __init__(self) -> None:
        self.password_helper = pbkdf2_sha256
        super().__init__(Profile)


    async def create_user(
            self,
            session: AsyncSession,
            in_obj: UserCreate | None = None,
            file: UploadFile | None = None,
            *,
            commit: bool = True,
            refresh_attribute_names: Iterable[str] | None = None,
            **attrs: Any,
    ) -> Profile:

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
                file = await file_manager.save_file(file)
            except Exception:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Could not upload file')

        create_data['photo_url'] = file
        db_obj: Profile = self.model(**create_data)
        account = Account(login=in_obj.username, password=in_obj.password,
                type='password'
                )
        token = Token(token=token_urlsafe(32))
        account.token = token
        db_obj.accounts.append(account)

        session.add(db_obj)

        await self.save(session, commit=commit)

        await session.refresh(db_obj, attribute_names=refresh_attribute_names)
        return db_obj




user_manager = UsersManager()