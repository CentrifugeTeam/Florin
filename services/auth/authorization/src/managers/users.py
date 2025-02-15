from typing import Iterable, Any
from fastapi import UploadFile, HTTPException
from fastapi_sqlalchemy_toolkit.model_manager import ModelManager
from  fastapi_libkit.responses import ErrorModel
from sqlmodel.ext.asyncio.session import AsyncSession
from ..schemas.users import UserCreate
from ..db import User
from starlette import status
from passlib.hash import pbkdf2_sha256
from ..adapters.files import file_manager

CouldUploadFileHTTPException = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Could not upload file')


def to_openapi(exception: HTTPException):
    return {exception.status_code: {
        'detail': exception.detail,
        'headers': exception.headers,
        'description': exception.detail,
        'model': ErrorModel
    }
    }

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
        create_data['username'] = in_obj.login
        await self.run_db_validation(session, in_obj=create_data)

        create_data['type'] = 'password'
        db_obj: User = self.model(**create_data)


        if in_obj.photo is not None:
            try:
                in_obj.photo = await file_manager.save_file(in_obj.photo, bucket='out-photos', folder=db_obj.id)
            except Exception:
                raise CouldUploadFileHTTPException

        db_obj.photo_url = in_obj.photo

        session.add(db_obj)

        await self.save(session, commit=commit)

        await session.refresh(db_obj, attribute_names=refresh_attribute_names)
        return db_obj



user_manager = UsersManager()