from http import HTTPStatus
from fastapi import APIRouter
from src.models.user_model import (
    UserResponse, User, UserResponseList, 
    Message, UserUpdate
)
from src.utils.responses import responses
from src.utils.types import T_Session, T_CurrentUser
from src.service.user_service import (
    create_user_service, get_all_users_service, get_user_by_id_service,
    delete_user_by_id_service, update_user_service
)
from src.utils.validations import authorize_user, is_admin
from src.models.exceptions import ForbiddenException
from src.utils.logging import logger


router = APIRouter(prefix='/user', tags=['users'])


@router.post(
    '', 
    response_model=UserResponse,
    status_code=HTTPStatus.CREATED,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error']
    }
)
def create_user(user: User, session: T_Session) -> UserResponse:
    logger.info(f'user_controller.py - User data recived - {user.username}')
    created_user = create_user_service(user, session)
    return created_user


@router.get(
    '/list',
    response_model=UserResponseList,
    status_code=HTTPStatus.OK,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unauthorized'],
        **responses['forbidden']
    }
)
def get_users(
    session: T_Session, 
    current_user: T_CurrentUser,
    offset: int = 0, limit: int = 100
) -> list[UserResponse]:
    if not is_admin(current_user, session):
        raise ForbiddenException(detail='User not allowed to access this resource')
    users = get_all_users_service(offset, limit, session)
    return {'users': users}


@router.get(
    '/{user_id}',
    response_model=UserResponse,
    status_code=HTTPStatus.OK,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unauthorized'],
        **responses['forbidden']
    }   
)
def get_user_by_id(
    user_id: int, session: T_Session, 
    current_user: T_CurrentUser
) -> UserResponse:
    if not is_admin(current_user, session):
        authorize_user(current_user.id, user_id)
    return get_user_by_id_service(user_id, session)


@router.delete(
    '/{user_id}',
    response_model=Message,
    status_code=HTTPStatus.OK,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unauthorized'],
        **responses['forbidden']
    }
)
def delete_user_by_id(
    user_id: int, session: T_Session, 
    current_user: T_CurrentUser
) -> Message:
    user_is_admin = is_admin(current_user, session)
    if not user_is_admin:
        authorize_user(current_user.id, user_id)
    user = get_user_by_id_service(user_id, session)
    if user_is_admin and user.id == current_user.id:
        raise ForbiddenException(detail='It is not possible to delete the admin user.')
    return delete_user_by_id_service(user_id, session)


@router.put(
    '/{user_id}',
    response_model=UserResponse,
    status_code=HTTPStatus.OK,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unauthorized'],
        **responses['forbidden']
    } 
)
def update_user(
    user_id: int, user_data: UserUpdate, 
    session: T_Session, 
    current_user: T_CurrentUser
) -> UserResponse:
    if not is_admin(current_user, session):
        authorize_user(current_user.id, user_id)  
    logger.info(f'user_controller.py - User data received (update)')
    return update_user_service(user_id, user_data, session)
