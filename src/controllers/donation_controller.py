from fastapi import APIRouter
from src.models.donation_model import DonationResponse, Donation, DonationResponseList
from http import HTTPStatus
from src.utils.responses import responses
from src.utils.types import T_CurrentUser, T_Session
from src.service.donation_service import create_donation_service, get_donations_service, delete_donation_by_id_service
from src.models.user_model import Message
from src.utils.validations import is_admin, authorize_delete_donation_operation
from src.models.exceptions import ForbiddenException


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


@router.get(
    '/list/{institution_id}', 
    response_model=DonationResponseList,
    status_code=HTTPStatus.OK,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unprocessable_entity']
    }
)
def get_donations(
    session: T_Session,
    current_user: T_CurrentUser, 
    institution_id: int,
    offset: int = 0, 
    limit: int = 100,
    max_amount: float = None,
    min_amount: float = None,
    min_date: int = None,
    max_date: int = None,
    payment_method: str = None   
) -> list[DonationResponse]:
    donations = get_donations_service(
        current_user.id, 
        institution_id, 
        session, 
        offset, 
        limit,
        max_amount,
        min_amount,
        min_date,
        max_date,
        payment_method
    )
    return {'donations': donations}


@router.delete(
    '/{donation_id}',
    response_model=Message,
    status_code=HTTPStatus.OK,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unauthorized'],
        **responses['forbidden']
    }
)
def delete_donation_by_id(
    donation_id: int, 
    session: T_Session, 
    current_user: T_CurrentUser
) -> Message:
    if not is_admin(current_user, session):
        authorize_delete_donation_operation(
            session, 
            donation_id, 
            current_user.id
        )
    return delete_donation_by_id_service(donation_id, session)
