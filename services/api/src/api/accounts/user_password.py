from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from fastapi import status, Request, Body, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_libkit.responses import  not_found_response, bad_request_response
from ...deps import get_session
from ...schemas.profiles import ProfileRead
from ...managers import user_manager

r = APIRouter(prefix="/password")


@r.post(
    "/forgot",
    status_code=status.HTTP_204_NO_CONTENT,
    name="reset:forgot_password",
    responses={
        **not_found_response,
    }
)
async def forgot_password(
        email: EmailStr = Body(..., embed=True),
        session: AsyncSession = Depends(get_session),
):
    """
    Отправляет письмо с ссылкой для сброса пароля пользователю.

    :param email: Электронная почта пользователя.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Ответ без содержимого тела.
    """
    user = await user_manager.get_or_404(session, email=email)
    token = await user_manager.forgot_password(session, user)

    # TODO send to notification service
    # await smtp_message.asend_email(
    #     email,
    #     Message(url_for_button=f'{settings.DOMAIN_URI}/change_pass/?token={token}', title='Заменить пароль', text_on_button='Кнопка',
    #             text='Востановление пароля')
    # )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@r.post(
    "/reset",
    name="reset:reset_password",
    responses={
        **bad_request_response,
    },
    response_model=ProfileRead,
)
async def reset_password(
        token: str = Body(...),
        password: str = Body(...),
        session: AsyncSession = Depends(get_session),
):
    """
    Сбрасывает пароль пользователя по токену.

    :param token: Токен для сброса пароля.
    :param password: Новый пароль пользователя.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Объект пользователя после сброса пароля.
    """
    return await user_manager.reset_password(session,token, password)

