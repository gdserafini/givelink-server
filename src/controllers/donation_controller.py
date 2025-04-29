from fastapi import APIRouter
from src.models.donation_model import DonationResponse, Donation
from http import HTTPStatus
from src.utils.responses import responses
from src.utils.types import T_CurrentUser, T_Session
from src.service.donation_service import create_donation_service


router = APIRouter(prefix='/donation', tags=['Donations'])


@router.post(
    '',
    response_model=DonationResponse,
    status_code=HTTPStatus.CREATED,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unauthorized'],
        **responses['unprocessable_entity']
    }
)
def create_donation(
    session: T_Session,
    current_user: T_CurrentUser,
    donation: Donation
) -> DonationResponse:
    created_donation = create_donation_service(
        donation, session, current_user
    )
    return created_donation