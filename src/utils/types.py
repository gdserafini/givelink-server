from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.service.session import get_session
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


T_Token = Annotated[str, Depends(oauth2_scheme)] 
T_Session = Annotated[Session, Depends(get_session)]


#Is needed to use this func to avoid a circular import error
#On T_CurrentUser data type (Depends)
def resolve_get_current_user(session: T_Session, token: T_Token):
    from src.service.security import get_current_user
    return get_current_user(session, token)


T_OAuth2From = Annotated[OAuth2PasswordRequestForm, Depends()]
T_CurrentUser = Annotated[dict, Depends(resolve_get_current_user)]
