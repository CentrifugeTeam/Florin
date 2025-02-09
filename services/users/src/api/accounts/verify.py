from fastapi import APIRouter, Body, Depends, HTTPException, Request, status, Response
from pydantic import EmailStr

from sqlmodel.ext.asyncio.session import AsyncSession
from web.app.exceptions import UserAlreadyVerifiedException
from web.app.schemas import ReadUser

from fastapi_libkit.responses import  not_found_response, bad_request_response, ErrorModel
from ..managers import user_manager
from ..deps import get_session

r = APIRouter(prefix="/verify")


@r.post(
    "/request",
    status_code=status.HTTP_204_NO_CONTENT,
    name="verify:request-token",
    responses={
        **not_found_response,
        **bad_request_response
    }
)
async def request_verify_token(
        request: Request,
        email: EmailStr = Body(..., embed=True),
        session: AsyncSession = Depends(get_session),
):
    """
    Отправляет письмо с инструкциями по верификации на указанный email.

    :param email: Email пользователя.
    :param session: Сессия базы данных.
    """
    user = await user_manager.get_or_404(session, email=email)
    if user.is_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='VERIFY_USER_ALREADY_VERIFIED')
    token = await user_manager.forgot_password(session, user)

    # TODO send to notification service
    # await smtp_message.asend_email(
    #     email,
    #     Message(url_for_button=f'{settings.DOMAIN_URI}/change_pass/?token={token}', title='Заменить пароль', text_on_button='Кнопка',
    #             text='Востановление пароля')
    # )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@r.post(
    "/",
    response_model=ReadUser,
    name="verify:verify",
    responses={
        **not_found_response,
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        'VERIFY_USER_ALREADY_VERIFIED': {
                            "summary": "The user is already verified.",
                            "value": {
                                "detail": 'VERIFY_USER_ALREADY_VERIFIED'
                            },
                        },
                    }
                }
            },
        }
    },
)
async def verify(
        request: Request,
        token: str = Body(..., embed=True),
        session: AsyncSession = Depends(get_session),
):
    """
    Верифицирует пользователя по токену.

    :param token: Токен для верификации.
    :param session: Сессия базы данных.
    :return: Объект пользователя после верификации.
    """
    try:
        return await user_manager.verify(session, token)
    except UserAlreadyVerifiedException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='VERIFY_USER_ALREADY_VERIFIED')
