from zoneinfo import ZoneInfo
from pwdlib import PasswordHash
from datetime import datetime, timedelta
from jwt import decode, encode
from sqlalchemy import select
from config.settings import Settings
from src.models.exceptions import InvalidLoginException
from src.models.db_schemas import UserModel
from jwt.exceptions import PyJWTError, ExpiredSignatureError
from src.utils.types import T_Session, T_Token


pwd_context = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str, hashed_password: str
) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(
        ZoneInfo('UTC')) + \
        timedelta(minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    return encode(
        to_encode, 
        Settings().SECRET_KEY, algorithm=Settings().ALGORITHM
    )


def get_current_user(session: T_Session, token: T_Token) -> UserModel:
    try:
        payload = decode(
            token, Settings().SECRET_KEY, 
            algorithms=[Settings().ALGORITHM]
        )
        email = payload.get('sub')
        if not email:
            raise InvalidLoginException(detail='Invalid token.')
        user_db = session.scalar(
            select(UserModel).where(UserModel.email == email)
        )
        if not user_db:
            raise InvalidLoginException(detail='User not found.')
        return user_db
    except ExpiredSignatureError:
        raise InvalidLoginException(detail='Expired token.')
    except PyJWTError:
        raise InvalidLoginException(detail='Invalid token.')