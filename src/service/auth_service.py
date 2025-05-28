from sqlalchemy import select
from src.models.exceptions import InvalidLoginException
from src.models.db_schemas import UserModel
from sqlalchemy.orm import Session
from src.service.security import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from src.models.token_model import Token
from http import HTTPStatus
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from src.utils.logging import logger


def login_service(
    session: Session, 
    form_data: OAuth2PasswordRequestForm
) -> Token:
    user = session.scalar(
        select(UserModel).where(UserModel.username == form_data.username)
    )
    if not user or \
            not verify_password(form_data.password, user.password):
        logger.info(f'auth_service.py - Error: Invalid credential - {form_data.username}')
        raise InvalidLoginException(
            detail='Invalid credentials.',
            status_code=HTTPStatus.BAD_REQUEST
        )
    else:
        token_jwt = create_access_token({'sub': user.email})
        logger.info(f'auth_service.py - Token JWT created - {form_data.username}')
        return Token(
            token_type='Bearer',
            access_token=token_jwt
        )
    

def refresh_access_token_service(user: UserModel) -> Token:
    try:
        new_access_token = create_access_token(
            data={'sub': user.email}
        )
        logger.info(f'auth_service.py - Token JWT refresehd - {user.username}')
        return Token(
            token_type='Bearer',
            access_token=new_access_token
        )
    except ExpiredSignatureError:
        logger.info(f'auth_service.py - Error: Expired token - {user.username}')
        raise InvalidLoginException(detail='Expired token.')
    except PyJWTError:
        logger.info(f'auth_service.py - Error: Invalid token - {user.username}')
        raise InvalidLoginException(detail='Invalid token.')
