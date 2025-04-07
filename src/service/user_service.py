from src.models.user_model import User, UserResponse
from sqlalchemy.orm import Session
from src.models.db_schemas import UserModel, RolesModel
from sqlalchemy import select
from src.models.exceptions import UserAlreadyExistsException
from src.service.security import get_password_hash


def create_user_service(user: User, session: Session) -> UserResponse:
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
        role_id=0
    )
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    user_db_role = session.scalar(
        select(RolesModel).where(RolesModel.id == user_db.role_id)
    )
    return UserResponse(
        id=user_db.id,
        username = user_db.username,
        email = user_db.email,
        avatar_url = user_db.avatar_url,
        role = user_db_role.role 
    )