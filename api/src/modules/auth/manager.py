from typing import Iterable, Any
from fastapi import HTTPException
from fastapi_sqlalchemy_toolkit.model_manager import ModelManager
from fastapi_libkit.responses import ErrorModel
from sqlmodel.ext.asyncio.session import AsyncSession
from .scheme import UserCreate
from ...db import User, Token
from starlette import status
from passlib.hash import pbkdf2_sha256
from ..files.adapter import file_adapter as file_adapter
from typing import Optional
from sqlmodel import select

CouldUploadFileHTTPException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Could not download a file"
)


class UsersManager(ModelManager):
    def __init__(self) -> None:
        self.password_helper = pbkdf2_sha256
        super().__init__(User)

    async def create_user(
        self,
        session: AsyncSession,
        in_obj: UserCreate,
        *,
        commit: bool = True,
        refresh_attribute_names: Iterable[str] | None = None,
        **attrs: Any,
    ) -> User:
        in_obj.password = self.password_helper.hash(in_obj.password)
        create_data = in_obj.model_dump()
        create_data.update(attrs)

        # Добавляем дефолтные значения полей для валидации уникальности
        for field, default in self.defaults.items():
            if field not in create_data:
                create_data[field] = default

        await self.run_db_validation(session, in_obj=create_data)

        create_data["type"] = "password"
        db_obj: User = self.model(**create_data)

        if in_obj.photo is not None:
            try:
                in_obj.photo = await file_adapter.save_file(
                    in_obj.photo, bucket_name="profiles"
                )
            except Exception as e:
                raise CouldUploadFileHTTPException

        db_obj.photo_url = in_obj.photo

        session.add(db_obj)

        await self.save(session, commit=commit)

        await session.refresh(db_obj, attribute_names=refresh_attribute_names)
        return db_obj

    async def save_user_token(self, session: AsyncSession, user: User, token: str):
        token_db = Token(token=token, user_id=user.id)
        session.add(token_db)
        await session.commit()

    async def create_or_get_user(
        self,
        session: AsyncSession,
        user_data: dict,
        *,
        commit: bool = True,
        refresh_attribute_names: Optional[Iterable[str]] = None,
    ) -> User:
        """
        Метод для создания или получения пользователя из базы данных по email.
        Если пользователь с данным email существует, то он будет возвращен.
        Если нет — будет создан новый пользователь.
        """
        email = user_data.get("email")

        query = select(User).where(User.email == email)
        user_result = await session.exec(query)
        user = user_result.first()

        if user:
            return user

        # Создание нового пользователя
        create_data = {
            "email": email,
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "username": "Пользователь",
            "photo_url": user_data.get("picture"),
            "type": "sso",
            "password": None,
        }

        db_obj: User = self.model(**create_data)
        session.add(db_obj)
        await self.save(session, commit=commit)

        await session.refresh(db_obj, attribute_names=refresh_attribute_names)
        return db_obj


user_manager = UsersManager()
