from fastapi import HTTPException
from fastapi_libkit.responses import ErrorModel


def to_openapi(exception: HTTPException):
    return {
        exception.status_code: {
            "detail": exception.detail,
            "headers": exception.headers,
            "description": exception.detail,
            "model": ErrorModel,
        }
    }
