from fastapi import APIRouter
from src.utils.responses import responses
from http import HTTPStatus
from src.utils.types import T_CurrentUser, T_Session
from src.models.donor_model import (
    Donor, DonorResponse, DonorResponseList,
    DonorUpdate
)
from src.service.donor_service import (
    create_donor_service, get_donors_service, get_donor_by_id_service,
    delete_donor_by_id_service, update_donor_service, get_donors_logged_service
)
from src.models.user_model import Message
from src.utils.validations import authorize_donor_operation, is_admin
from src.utils.logging import logger


router = APIRouter(prefix='/donor', tags=['donors'])


@router.get(
    '/list/me',
    response_model=DonorResponseList,
    status_code=HTTPStatus.OK,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unauthorized']
    }
)
def get_donations_logged(
    session: T_Session,
    current_user: T_CurrentUser
) -> list[DonorResponse]:
    logger.info('Getting donors - Logged user')
    donations = get_donors_logged_service(
        session, 
        current_user.id
    )
    return {
        'donors': donations
    }


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
    logger.info('Creating donor entity')
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
    logger.info('Getting donors')
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
    logger.info('Getting donor - By id')
    return get_donor_by_id_service(session, donor_id)


@router.delete(
    '/{donor_id}',
    response_model=Message,
    status_code=HTTPStatus.OK,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unauthorized'],
        **responses['forbidden']
    }
)
def delete_donor_by_id(
    donor_id: int, 
    session: T_Session, 
    current_user: T_CurrentUser
) -> Message:
    user_is_admin = is_admin(current_user, session)
    if not user_is_admin:
        authorize_donor_operation(current_user.id, donor_id, session)
    logger.info('Deleting donor - By id - Logged user')
    return delete_donor_by_id_service(donor_id, session)
    

@router.put(
    '/{donor_id}',
    response_model=DonorResponse,
    status_code=HTTPStatus.OK,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unauthorized'],
        **responses['forbidden']
    } 
)
def update_donor(
    donor_id: int, 
    donor_data: DonorUpdate, 
    session: T_Session, 
    current_user: T_CurrentUser
) -> DonorResponse:
    if not is_admin(current_user, session):
        authorize_donor_operation(current_user.id, donor_id, session)
    logger.info('Updating donor - Logged user')
    return update_donor_service(donor_id, donor_data, session)
