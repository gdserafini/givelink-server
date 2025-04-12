from src.models.user_model import User, UserResponse, Message
from sqlalchemy.orm import Session
from src.models.db_schemas import UserModel, RolesModel
from sqlalchemy import select
from src.models.exceptions import UserAlreadyExistsException, UserNotFoundException
from src.service.security import get_password_hash
from src.models.role_model import RoleIdEnum
from src.utils.validations import validate_user_data


def create_user_service(user: User, session: Session) -> UserResponse:
    validate_user_data(user)
    result = session.scalar(
        select(UserModel).where(
            (UserModel.username == user.username) |
            (UserModel.email == user.email)
        )
    )
    if result:
        if result.username == user.username:
            raise UserAlreadyExistsException(username=user.username)
        elif result.email == user.email:
            raise UserAlreadyExistsException(email=user.email)
    user_db = UserModel(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
        avatar_url=user.avatar_url,
        role_id=RoleIdEnum.USER.value
    )
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return cast_to_user_response(user_db, session)


def cast_to_user_response(
    user: UserModel, session: Session
) -> UserResponse:
    user_db_role = session.scalar(
        select(RolesModel).where(RolesModel.id == user.role_id)
    )
    return UserResponse(
        id=user.id,
        username = user.username,
        email = user.email,
        avatar_url = user.avatar_url,
        role = user_db_role.role 
    )


def get_all_users_service(
    offset: int, limit: int, session: Session
) -> list[UserResponse]:
    if offset < 0 or limit < 0 or \
        type(offset) != int or type(limit) != int:
        raise ValueError('Invalid params.')
    users = session.scalars(
        select(UserModel).offset(offset).limit(limit)
    ).all()
    return [
        cast_to_user_response(user, session) for user in users
    ]


def get_user_by_id_service(
        user_id: int, session: Session, cast: bool = True
) -> UserResponse:
    user = session.scalar(
        select(UserModel).where(UserModel.id == user_id)
    )
    if not user:
        raise UserNotFoundException(user_id=user_id)
    if cast: return cast_to_user_response(user, session)
    else: return user


def delete_user_by_id_service(
    user_id: int, session: Session
) -> Message:
    user = get_user_by_id_service(user_id, session, False)
    session.delete(user)
    session.commit()
    return Message(
        message=f'User id={user_id} deleted successfully'
    )


def update_user_service(
    user_id: int, user: User, session: Session
) -> UserResponse:
    validate_user_data(user)
    user_db = get_user_by_id_service(user_id, session, False)
    if user.username: 
        result = session.scalar(
            select(UserModel).where(
                (UserModel.username == user.username)
            )
        )
        if result:
            raise UserAlreadyExistsException(detail='Username already in use.')
        else:
            user_db.username = user.username
    if user.password: user_db.password = get_password_hash(user.password)
    if user.avatar_url: user_db.avatar_url = user.avatar_url
    session.commit()
    session.refresh(user_db)
    return cast_to_user_response(user_db, session)
