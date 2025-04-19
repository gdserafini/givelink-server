from src.models.donor_model import Donor, DonorResponse
from src.models.user_model import User
from sqlalchemy.orm import Session
from src.models.db_schemas import DonorModel, UserModel
from sqlalchemy import select
from src.models.exceptions import (
    DonorAlreadyExistsException, InvalidFormException, DonorNotFoundException
)


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

def get_donors_service(
    session: Session,
    offset: int,
    limit: int
) -> list[DonorResponse]:
    if offset < 0 or limit < 0 or \
        type(offset) != int or type(limit) != int:
        raise ValueError('Invalid params.')
    donors = session.scalars(
        select(DonorModel).offset(offset).limit(limit)
    ).all()
    return [
        cast_to_donor_response(donor, session) for donor in donors
    ]


def cast_to_donor_response(
    donor: DonorModel, 
    session: Session
) -> DonorResponse:
    donor_username = session.scalar(
        select(UserModel).where(
            UserModel.id == donor.user_id
        )
    ).username
    return DonorResponse(
        id=donor.id,
        name=donor.name,
        avatar_url=donor.avatar_url,
        cpf_cnpj=donor.cpf_cnpj,
        username=donor_username
    )


def get_donor_by_id_service(
    session: Session, 
    donor_id: int,
    cast: bool = True
) -> DonorResponse:
    donor = session.scalar(
        select(DonorModel).where(
            DonorModel.id == donor_id
        )
    )
    if not donor:
        raise DonorNotFoundException(donor_id=donor_id)
    if cast: return cast_to_donor_response(donor, session)
    else: return donor    
