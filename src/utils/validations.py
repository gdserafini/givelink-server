from src.models.exceptions import ForbiddenException, InvalidDataException
from src.models.user_model import User
import re
from src.models.db_schemas import UserModel, RolesModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models.role_model import RoleEnum
from src.models.donor_model import Donor


def validate_donor_data(donor: Donor) -> None:
    ...


def authorize_user(current_id: int, id: int) -> None:
    if current_id != id:
        raise ForbiddenException(
            detail='User not allowed to access/use this resource.'
        )
    

def validate_user_data(user: User):
    if user.username:
        if not re.fullmatch(r'[a-z]{3,255}', user.username):
            raise InvalidDataException(invalid_data=user.username)
    if user.password:
        if len(user.password) < 8 or len(user.password) > 255\
                or not re.search(r"[A-Z]", user.password)\
                or not re.search(r"[0-9]", user.password)\
                or not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]\\\/]", user.password):
            raise InvalidDataException(invalid_data='password')


def is_admin(user: UserModel, session: Session) -> bool:
    role = session.scalar(
        select(RolesModel).where(
            RolesModel.id == user.role_id
        )
    )
    return role.role == RoleEnum.ADMIN.value
