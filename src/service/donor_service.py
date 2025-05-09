from src.models.donor_model import Donor, DonorResponse, DonorUpdate
from src.models.user_model import User, Message
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
    if user.username == 'admin':
        raise InvalidFormException(
            detail='Not allowed to create a donor for the admin user.'
        )
    user_username = user.username
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
        id=donor_db.id,
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


def delete_donor_by_id_service(
    id: int, 
    session: Session
) -> Message:
    donor = get_donor_by_id_service(session, id, False)
    session.delete(donor)
    session.commit()
    return Message(
        message=f'Donor: {id} deleted successfuly.'
    )


def update_donor_service(
    donor_id: int, 
    donor_data: DonorUpdate,
    session: Session
) -> DonorResponse:
    donor = get_donor_by_id_service(session, donor_id, False)
    if donor_data.name: donor.name = donor_data.name
    if donor_data.avatar_url: donor.avatar_url = donor_data.avatar_url
    session.commit()
    session.refresh(donor)
    return cast_to_donor_response(donor, session)


def get_donors_logged_service(
    session: Session, user_id: int
) -> list[DonorResponse]:
    donors = session.scalars(
        select(
            DonorModel
        ).where(
            DonorModel.user_id == user_id
        )
    ).all()
    return [
        cast_to_donor_response(donor, session) for donor in donors
    ]
