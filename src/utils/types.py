from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from src.service.session import get_session
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


T_Session = Annotated[Session, Depends(get_session)]
