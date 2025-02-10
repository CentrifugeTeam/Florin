from fastapi import HTTPException


class FileException(Exception):
    pass

class JwtAuthError(Exception):
    pass


class UnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Unauthorized")

class ForbidException(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="Forbidden")


class InvalidResetPasswordToken(Exception):
    pass


class UserAlreadyVerifiedException(Exception):
    pass


class GenerationFileException(Exception):
    pass