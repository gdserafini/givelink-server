from src.models.donation_model import Donation, DonationResponse
from sqlalchemy.orm import Session
from src.models.db_schemas import DonationModel, DonorModel, InstitutionModel
from sqlalchemy import select
from src.models.user_model import User
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
