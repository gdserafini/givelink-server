from http import HTTPStatus
from fastapi import APIRouter
from src.models.user_model import UserResponse, User
from src.utils.responses import responses
from src.utils.types import T_Session
from src.service.user_service import create_user_service


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
    created_user = create_user_service(user, session)
    return created_user