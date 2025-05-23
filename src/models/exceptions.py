from fastapi import HTTPException
from http import HTTPStatus


class UserNotFoundException(HTTPException): # pragma: no cover
    def __init__(self, 
        status_code: int = HTTPStatus.NOT_FOUND, 
        datail: str = 'User not found',
        user_id: int = None
    ):
        msg = f'User not found: id = {user_id}'
        super().__init__(status_code=status_code, detail=msg)


class DonorNotFoundException(HTTPException): # pragma: no cover
    def __init__(self, 
        status_code: int = HTTPStatus.NOT_FOUND, 
        donor_id: int = None
    ):
        msg = f'Donor not found: id = {donor_id}'
        super().__init__(status_code=status_code, detail=msg)


class InstitutionNotFoundException(HTTPException): # pragma: no cover
    def __init__(self, 
        status_code: int = HTTPStatus.NOT_FOUND, 
        institution_id: int = None
    ):
        msg = f'Institution not found: id = {institution_id}'
        super().__init__(status_code=status_code, detail=msg)



class TaskNotFoundException(HTTPException): # pragma: no cover
    def __init__(self, 
        status_code: int = HTTPStatus.NOT_FOUND, 
        datail: str = 'Task not found.',
        task_id: int = None
    ):
        msg = f'Task not found: id = {task_id}'
        super().__init__(status_code=status_code, detail=msg)


class UserAlreadyExistsException(HTTPException): # pragma: no cover
    def __init__(self, 
        status_code: int = HTTPStatus.BAD_REQUEST, 
        detail: str = 'User already exists',
        username: str = None,
        email: str = None
    ):
        msg = f'User already exists: username = {username}, email = {email}'
        super().__init__(status_code=status_code, detail=msg)


class DonorAlreadyExistsException(HTTPException): # pragma: no cover
    def __init__(self, 
        status_code: int = HTTPStatus.BAD_REQUEST, 
        donor: str = None
    ):
        msg = f'Donor already exists: CPF/CNPJ {donor}'
        super().__init__(status_code=status_code, detail=msg)


class InstitutionAlreadyExistsException(HTTPException): # pragma: no cover
    def __init__(self, 
        status_code: int = HTTPStatus.BAD_REQUEST, 
        institution: str = None
    ):
        msg = f'Institution already exists: CNPJ {institution}'
        super().__init__(status_code=status_code, detail=msg)


class InvalidLoginException(HTTPException): # pragma: no cover
    def __init__(self, 
        status_code: int = HTTPStatus.UNAUTHORIZED, 
        detail: str = 'Invalid login credentials.'
    ):
        super().__init__(status_code=status_code, detail=detail)


class ForbiddenException(HTTPException): # pragma: no cover
    def __init__(self, 
        status_code: int = HTTPStatus.FORBIDDEN, 
        detail: str = 'Forbidden'
    ):
        super().__init__(status_code=status_code, detail=detail)


class DatabaseConnectionError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

    def __str__(self):
        return super().__str__()
    

class InvalidDataException(Exception):
    def __init__(
        self,
        invalid_data: str = None
    ):
        status_code: int = HTTPStatus.UNPROCESSABLE_ENTITY
        message: str = 'Invalid data: '
        detail = f'{status_code} - {message}{invalid_data}'
        super.__init__(status_code=status_code, detail=detail)


class InvalidFormException(HTTPException): # pragma: no cover
    def __init__(self, 
        status_code: int = HTTPStatus.UNPROCESSABLE_ENTITY, 
        detail: str = 'Invalid data.'
    ):
        super().__init__(status_code=status_code, detail=detail)
