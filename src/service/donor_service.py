from src.models.donor_model import Donor, DonorResponse
from src.models.user_model import User
from sqlalchemy.orm import Session
from src.models.db_schemas import DonorModel, UserModel
from sqlalchemy import select
from src.models.exceptions import DonorAlreadyExistsException, InvalidFormException


def create_donor_service(
    donor: Donor, user: User, session: Session
) -> DonorResponse:
    result = session.scalar(
        select(DonorModel).where(
            DonorModel.cpf_cnpj == donor.cpf_cnpj
        )
    )
    if result:
        raise DonorAlreadyExistsException(donor=donor.cpf_cnpj)
    if not donor.username and user.username == 'admin':
        raise InvalidFormException(
            detail='Not allowed to create a donor for the admin user.'
        )
    user_username = donor.username if donor.username else user.username
    user_db = session.scalar(
        select(UserModel).where(
            UserModel.username == user_username
        )
    )
    donor_db = DonorModel(
        name=donor.name,
        avatar_url=donor.avatar_url,
        cpf_cnpj=donor.cpf_cnpj,
        user_id=user_db.id
    )    
    session.add(donor_db)
    session.commit()
    session.refresh(donor_db)
    return DonorResponse(
        name=donor_db.name,
        avatar_url=donor_db.avatar_url,
        cpf_cnpj=donor_db.cpf_cnpj,
        username=user_db.username
    )
