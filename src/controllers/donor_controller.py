from fastapi import APIRouter
from src.utils.responses import responses
from http import HTTPStatus
from src.utils.types import T_CurrentUser, T_Session
from src.models.donor_model import Donor, DonorResponse, DonorResponseList
from src.service.donor_service import create_donor_service, get_donors_service, get_donor_by_id_service


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


@router.get(
    '/list', 
    response_model=DonorResponseList,
    status_code=HTTPStatus.OK,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unprocessable_entity']
    }
)
def get_donors(
    session: T_Session, 
    offset: int = 0, 
    limit: int = 100    
) -> list[DonorResponse]:
    donors = get_donors_service(session, offset, limit)
    return {'donors': donors}


@router.get(
    '/{donor_id}', 
    response_model=DonorResponse,
    status_code=HTTPStatus.OK,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unprocessable_entity']
    }
)
def get_donors(
    donor_id: int,
    session: T_Session  
) -> DonorResponse:
    return get_donor_by_id_service(session, donor_id)
