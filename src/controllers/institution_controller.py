from fastapi import APIRouter
from src.utils.responses import responses
from http import HTTPStatus
from src.utils.types import T_CurrentUser, T_Session
from src.models.institution_model import (
    InstitutionResponse, Institution, InstitutionResponseList,
    InstitutionUpdate
)
from src.service.institution_service import (
    create_institution_service, get_institutions_service, get_institution_by_id_service,
    delete_institution_by_id_service, update_institution_service, get_institutions_logged_service
)
from src.models.user_model import Message
from src.utils.validations import is_admin, authorize_institution_operation 
from src.utils.logging import logger


router = APIRouter(prefix='/institution', tags=['Institutions'])


@router.post(
    '', 
    response_model=InstitutionResponse,
    status_code=HTTPStatus.CREATED,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unauthorized'],
        **responses['unprocessable_entity']
    }
)
def create_institution(
    session: T_Session,
    current_user: T_CurrentUser,
    institution: Institution
) -> InstitutionResponse:
    created_institution = create_institution_service(
        institution, current_user, session
    )
    logger.info(f'institution_controller.py - Instituition data received - {institution.name}')
    return created_institution


@router.get(
    '/list/me',
    response_model=InstitutionResponseList,
    status_code=HTTPStatus.OK,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unauthorized']
    }
)
def get_institutions_logged(
    session: T_Session,
    current_user: T_CurrentUser,
    sector: str = None
) -> list[InstitutionResponse]:
    institutions = get_institutions_logged_service(
        session, 
        current_user.id,
        sector
    )
    return {
        'institutions': institutions
    }


@router.get(
    '/list', 
    response_model=InstitutionResponseList,
    status_code=HTTPStatus.OK,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unprocessable_entity']
    }
)
def get_institutions(
    session: T_Session, 
    offset: int = 0, 
    limit: int = 100,
    sector: str = None
) -> list[InstitutionResponse]:
    institutions = get_institutions_service(
        session, 
        offset, 
        limit,
        sector
    )
    return {
        'institutions': institutions
    }


@router.get(
    '/{institution_id}', 
    response_model=InstitutionResponse,
    status_code=HTTPStatus.OK,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unprocessable_entity']
    }
)
def get_institution(
    institution_id: int,
    session: T_Session  
) -> InstitutionResponse:
    return get_institution_by_id_service(session, institution_id)


@router.delete(
    '/{institution_id}',
    response_model=Message,
    status_code=HTTPStatus.OK,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unauthorized'],
        **responses['forbidden']
    }
)
def delete_institution_by_id(
    institution_id: int, 
    session: T_Session, 
    current_user: T_CurrentUser
) -> Message:
    user_is_admin = is_admin(current_user, session)
    if not user_is_admin:
        authorize_institution_operation(current_user.id, institution_id, session)
    return delete_institution_by_id_service(institution_id, session)


@router.put(
    '/{institution_id}',
    response_model=InstitutionResponse,
    status_code=HTTPStatus.OK,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unauthorized'],
        **responses['forbidden']
    } 
)
def update_donor(
    institution_id: int, 
    institution_data: InstitutionUpdate, 
    session: T_Session, 
    current_user: T_CurrentUser
) -> InstitutionResponse:
    if not is_admin(current_user, session):
        authorize_institution_operation(current_user.id, institution_id, session)
    logger.info('institution_controller.py - Donor data received (update)')
    return update_institution_service(institution_id, institution_data, session)
