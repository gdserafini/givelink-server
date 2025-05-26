from http import HTTPStatus
from fastapi import APIRouter
from src.utils.responses import responses
from src.models.token_model import Token
from src.service.auth_service import login_service, refresh_access_token_service
from src.utils.types import T_OAuth2From, T_Session, T_CurrentUser
from src.utils.logging import logger


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/token',
    status_code=HTTPStatus.OK,
    response_model=Token,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unauthorized'],
        **responses['not_found'],
        **responses['bad_request']
    },
    description='Get a JWT token to authenticate using email and password.'
)
def login(session: T_Session,form_data: T_OAuth2From) -> Token:
    logger.info('Authenticating - JWT token')
    jwt_token = login_service(session, form_data)
    return jwt_token


@router.post(
    '/token/refresh',
    status_code=HTTPStatus.OK,
    response_model=Token,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unauthorized'],
        **responses['not_found'],
        **responses['bad_request']
    },
    description='Get a refreshed JWT token.'
)
def refresh_access_token(user: T_CurrentUser) -> Token:
    logger.info('Refreshing token - JWT')
    refreshed_jwt_token = refresh_access_token_service(user)
    return refreshed_jwt_token