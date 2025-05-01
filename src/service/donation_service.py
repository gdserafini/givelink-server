from src.models.donation_model import Donation, DonationResponse
from sqlalchemy.orm import Session
from src.models.db_schemas import DonationModel, DonorModel, InstitutionModel, UserModel
from sqlalchemy import select
from src.models.user_model import User, Message
from fastapi import HTTPException
from http import HTTPStatus


def create_donation_service(
    donation: Donation,
    session: Session,
    user: User
) -> DonationResponse:
    donor = session.scalar(
        select(DonorModel).where(
            DonorModel.id == donation.donor_id
        )
    )
    if user.id != donor.user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=f"Logged user and donor's user is different."
        )
    institution = session.scalar(
        select(InstitutionModel).where(
            InstitutionModel.id == donation.institution_id
        )
    )
    donation_db = DonationModel(
        amount = donation.amount,
        payment_method = donation.payment_method,
        donor_id = donation.donor_id,
        institution_id = donation.institution_id
    )
    session.add(donation_db)
    session.commit()
    session.refresh(donation_db)
    return DonationResponse(
        id = donation_db.id,
        amount = donation.amount,
        payment_method = donation.payment_method,
        date = donation_db.date,
        donor = donor.name,
        institution = institution.name
    )


def get_donations_service(
    user_id: int,
    institution_id: int,
    session: Session,
    offset: int,
    limit: int
) -> list[DonationResponse]:
    if offset < 0 or limit < 0 or \
        type(offset) != int or type(limit) != int:
        raise ValueError('Invalid params.')
    institution = session.scalar(
        select(InstitutionModel).where(
            InstitutionModel.id == institution_id
        )
    )
    user = session.scalar(
        select(UserModel).where(
            UserModel.id == user_id
        )
    )
    if institution.user_id != user_id and user.username != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.Forbidden,
            detail='User not allowed to access this resource.'
        )
    donations = session.scalars(
        select(DonationModel).offset(offset).limit(limit)
    ).all()
    return [
        cast_to_donation_response(donation, session) for donation in donations 
    ]


def cast_to_donation_response(
    donation: Donation, 
    session: Session
) -> DonationResponse:
    donor = session.scalar(
        select(DonorModel).where(
            DonorModel.id == donation.donor_id
        )
    )
    institution = session.scalar(
        select(InstitutionModel).where(
            InstitutionModel.id == donation.institution_id
        )
    )
    return DonationResponse(
        id=donation.id,
        amount=donation.amount,
        date=donation.date,
        payment_method=donation.payment_method,
        institution=institution.name,
        donor=donor.name
    )


def get_donation_by_id_service(
    session: Session, 
    donation_id: int,
    cast: bool = True
) -> DonationResponse:
    donation = session.scalar(
        select(DonationModel).where(
            DonationModel.id == donation_id
        )
    )
    if not donation:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Donation {donation_id} not found.'
        )
    if cast: return cast_to_donation_response(donation, session)
    else: return donation  


def delete_donation_by_id_service(
    id: int, 
    session: Session
) -> Message:
    donation = get_donation_by_id_service(session, id, False)
    session.delete(donation)
    session.commit()
    return Message(
        message=f'Donation: {id} deleted successfuly.'
    )