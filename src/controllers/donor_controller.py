from fastapi import APIRouter
from src.utils.responses import responses
from http import HTTPStatus
from src.utils.types import T_CurrentUser, T_Session
from src.models.donor_model import Donor, DonorResponse
from src.service.donor_service import create_donor_service


router = APIRouter(prefix='/donor', tags=['donors'])


@router.post(
    '', 
    response_model=DonorResponse,
    status_code=HTTPStatus.CREATED,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unauthorized'],
        **responses['unprocessable_entity']
    }
)
def create_donor(
    session: T_Session,
    current_user: T_CurrentUser,
    donor: Donor
) -> DonorResponse:
    created_donor = create_donor_service(
        donor, current_user, session
    )
    return created_donor
