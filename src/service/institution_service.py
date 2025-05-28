from src.models.user_model import User, Message
from sqlalchemy.orm import Session
from src.models.db_schemas import InstitutionModel, UserModel
from sqlalchemy import select
from src.models.exceptions import (
    InstitutionAlreadyExistsException, InvalidFormException, InstitutionNotFoundException
)
from src.models.institution_model import Institution, InstitutionResponse, InstitutionUpdate
from src.utils.logging import logger


def get_institutions_logged_service(
    session: Session, 
    user_id: int,
    sector: str = None
) -> list[InstitutionResponse]:
    if not sector:
        institutions = session.scalars(
            select(
                InstitutionModel
            ).where(
                InstitutionModel.user_id == user_id
            )
        ).all()
        return [
            cast_to_institution_response(inst, session) 
            for inst in institutions
        ]
    institutions = session.scalars(
        select(
            InstitutionModel
        ).where(
            (InstitutionModel.user_id == user_id) &
            (InstitutionModel.sector == sector)
        )
    ).all()
    logger.info('Institutions successfully found')
    return [
        cast_to_institution_response(inst, session) 
        for inst in institutions
    ]


def create_institution_service(
    institution: Institution, user: User, session: Session
) -> InstitutionResponse:
    result = session.scalar(
        select(InstitutionModel).where(
            InstitutionModel.cnpj == institution.cnpj
        )
    )
    if result:
        raise InstitutionAlreadyExistsException(institution=institution.cnpj)
    if user.username == 'admin':
        raise InvalidFormException(
            detail='Not allowed to create a institution for the admin user.'
        )
    user_username = user.username
    user_db = session.scalar(
        select(UserModel).where(
            UserModel.username == user_username
        )
    )
    institution_db = InstitutionModel(
        name=institution.name,
        avatar_url=institution.avatar_url,
        cnpj=institution.cnpj,
        user_id=user_db.id,
        sector=institution.sector
    )    
    session.add(institution_db)
    session.commit()
    session.refresh(institution_db)
    logger.info('Institution successfully created')
    return InstitutionResponse(
        id=institution_db.id,
        name=institution_db.name,
        avatar_url=institution_db.avatar_url,
        cnpj=institution_db.cnpj,
        username=user_db.username,
        sector=institution_db.sector
    )


def get_institutions_service(
    session: Session,
    offset: int,
    limit: int,
    sector: str
) -> list[InstitutionResponse]:
    if offset < 0 or limit < 0:
        raise ValueError("Invalid params.")
    query = select(InstitutionModel)
    if sector:
        query = query.where(InstitutionModel.sector == sector)
    query = query.offset(offset).limit(limit)
    institutions = session.scalars(query).all()
    logger.info('Institutions successfully found - By filters')
    return [
        cast_to_institution_response(institution, session)
        for institution in institutions
    ]


def cast_to_institution_response(
    institution: InstitutionModel, 
    session: Session
) -> InstitutionResponse:
    institution_username = session.scalar(
        select(UserModel).where(
            UserModel.id == institution.user_id
        )
    ).username
    return InstitutionResponse(
        id=institution.id,
        name=institution.name,
        avatar_url=institution.avatar_url,
        cnpj=institution.cnpj,
        username=institution_username,
        sector=institution.sector
    )


def get_institution_by_id_service(
    session: Session, 
    institution_id: int,
    cast: bool = True
) -> InstitutionResponse:
    institution = session.scalar(
        select(InstitutionModel).where(
            InstitutionModel.id == institution_id
        )
    )
    if not institution:
        raise InstitutionNotFoundException(institution_id=institution_id)
    logger.info('Institution successfully found')
    if cast: return cast_to_institution_response(institution, session)
    else: return institution
    

def delete_institution_by_id_service(
    id: int, 
    session: Session
) -> Message:
    institution = get_institution_by_id_service(session, id, False)
    session.delete(institution)
    session.commit()
    logger.info('Institution successfully deleted')
    return Message(
        message=f'Institution: {id} deleted successfuly.'
    )


def update_institution_service(
    institution_id: int, 
    institution_data: InstitutionUpdate,
    session: Session
) -> InstitutionResponse:
    institution = get_institution_by_id_service(session, institution_id, False)
    if institution_data.name: institution.name = institution_data.name
    if institution_data.avatar_url: institution.avatar_url = institution_data.avatar_url
    if institution_data.sector: institution.sector = institution_data.sector
    session.commit()
    session.refresh(institution)
    logger.info('Institution successfully updated')
    return cast_to_institution_response(institution, session)
