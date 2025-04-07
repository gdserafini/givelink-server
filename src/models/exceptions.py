from fastapi import HTTPException
from http import HTTPStatus


class DatabaseConnectionError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

    def __str__(self):
        return super().__str__()
    

class UserAlreadyExistsException(HTTPException): # pragma: no cover
    def __init__(self, 
        status_code: int = HTTPStatus.BAD_REQUEST, 
        detail: str = 'User already exists',
        username: str = None,
        email: str = None
    ):
        msg = f'User already exists: username = {username}, email = {email}'
        super().__init__(status_code=status_code, detail=msg)
