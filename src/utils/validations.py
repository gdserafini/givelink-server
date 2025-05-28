from src.models.exceptions import ForbiddenException, InvalidDataException
from src.models.user_model import User
import re
from src.models.db_schemas import UserModel, RolesModel, DonorModel, InstitutionModel, DonationModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models.role_model import RoleEnum
from src.utils.logging import logger


def authorize_user(current_id: int, id: int) -> None:
    if current_id != id:
        raise ForbiddenException(
            detail='User not allowed to access/use this resource.'
        )
    logger.info(f'validations.py - User authorized - {current_id}')
    


def authorize_donor_operation(
    current_id: int, 
    donor_id: int,
    session: Session
) -> None:
    donor = session.scalar(
        select(DonorModel).where(
            DonorModel.id == donor_id
        )
    )
    if donor.user_id != current_id:
        raise ForbiddenException(
            detail='User not allowed to access/use/delete this resource.'
        )
    logger.info(
        f'validations.py - User authorized for donor operation - {current_id} - {donor_id}'
    )
    

def authorize_institution_operation(
    current_id: int, 
    institution_id: int,
    session: Session
) -> None:
    institution = session.scalar(
        select(InstitutionModel).where(
            InstitutionModel.id == institution_id
        )
    )
    if institution.user_id != current_id:
        raise ForbiddenException(
            detail='User not allowed to access/use/delete this resource.'
        )
    logger.info(
        f'validations.py - User authorized for institution operation - {current_id} - {institution_id}'
    )



def validate_user_data(user: User):
    if user.username:
        if not re.fullmatch(r'[a-zA-Z]{3,255}', user.username):
            raise InvalidDataException(invalid_data=user.username)
    if user.password:
        if len(user.password) < 8 or len(user.password) > 255\
                or not re.search(r"[A-Z]", user.password)\
                or not re.search(r"[0-9]", user.password)\
                or not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]\\\/]", user.password):
            raise InvalidDataException(invalid_data='password')
    logger.info(
        f'validations.py - Valid user data - {user.username}'
    )


def is_admin(user: UserModel, session: Session) -> bool:
    role = session.scalar(
        select(RolesModel).where(
            RolesModel.id == user.role_id
        )
    )
    logger.info(
        f'validations.py - User authorized (ADMIN) - {user.username}'
    )
    return role.role == RoleEnum.ADMIN.value


def authorize_delete_donation_operation(
    session, 
    donation_id: int, 
    user_id: int
) -> None:
    user = session.scalar(
        select(UserModel).where(
            UserModel.id == user_id
        )
    )
    donation = session.scalar(
        select(DonationModel).where(
            DonationModel.id == donation_id
        )
    )
    institution = session.scalar(
        select(InstitutionModel).where(
            InstitutionModel.id == donation.institution_id
        )
    )
    if user.id != institution.user_id:
        raise ForbiddenException(
            detail='User not allowed to access this resource.'
        )
    logger.info(
        f'validations.py - User authorized for donation operation - {user_id} - {donation_id}'
    )
