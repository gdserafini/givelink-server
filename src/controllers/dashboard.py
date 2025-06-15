from http import HTTPStatus
from fastapi import APIRouter
from pydantic import BaseModel
from src.utils.responses import responses
from src.utils.types import T_Session, T_CurrentUser
from src.utils.logging import logger
from datetime import datetime
from src.models.db_schemas import DonationModel, DonorModel, InstitutionModel
from sqlalchemy import func, desc
from sqlalchemy.orm import aliased, Session
from src.utils.validations import is_admin
from fastapi import HTTPException
from http import HTTPStatus


router = APIRouter(prefix='/dashboard', tags=['Dashboard'])


class DashboardResponse(BaseModel):
    total: float
    donations_per_method: dict[str, int]
    top10_donors: dict[str, float]
    top10_institutions: dict[str, float]
    donations_per_sector: dict[str, int]


def get_total(
    session: Session, min_date: datetime, max_date: datetime
) -> float:
    total = session.query(func.coalesce(func.sum(DonationModel.amount), 0.0)).filter(
        DonationModel.date.between(min_date, max_date)
    ).scalar()
    return total


def get_donations_per_method(
    session: Session, min_date: datetime, max_date: datetime
) -> dict[str, int]:
    donations_per_method = dict(session.query(
        DonationModel.payment_method,
        func.count(DonationModel.id)
    ).filter(
        DonationModel.date.between(min_date, max_date)
    ).group_by(DonationModel.payment_method).all())
    return donations_per_method


def get_top10_donors(
    session: Session, min_date: datetime, max_date: datetime
) -> dict[str, float]:
    donor_alias = aliased(DonorModel)
    top10_donors = dict(session.query(
        donor_alias.name,
        func.sum(DonationModel.amount)
    ).join(
        donor_alias, donor_alias.id == DonationModel.donor_id
    ).filter(
        DonationModel.date.between(min_date, max_date)
    ).group_by(donor_alias.name)
     .order_by(desc(func.sum(DonationModel.amount)))
     .limit(10)
     .all())
    return top10_donors


def get_top10_institutions(
    session: Session, min_date: datetime, max_date: datetime
) -> dict[str, float]:
    institution_alias = aliased(InstitutionModel)
    top10_institutions = dict(session.query(
        institution_alias.name,
        func.sum(DonationModel.amount)
    ).join(
        institution_alias, institution_alias.id == DonationModel.institution_id
    ).filter(
        DonationModel.date.between(min_date, max_date)
    ).group_by(institution_alias.name)
     .order_by(desc(func.sum(DonationModel.amount)))
     .limit(10)
     .all())
    return top10_institutions


def get_donations_per_sector(
    session: Session, min_date: datetime, max_date: datetime
) -> dict[str, int]:
    donations_per_sector = dict(session.query(
        InstitutionModel.sector,
        func.count(DonationModel.id)
    ).join(
        InstitutionModel, InstitutionModel.id == DonationModel.institution_id
    ).filter(
        DonationModel.date.between(min_date, max_date)
    ).group_by(InstitutionModel.sector).all())
    return donations_per_sector


@router.get(
    '',
    response_model=DashboardResponse,
    status_code=HTTPStatus.OK,
    responses={
        **responses['bad_request'],
        **responses['internal_server_error'],
        **responses['unauthorized']
    }
)
def dashboard(
    session: T_Session, 
    user: T_CurrentUser,
    min_date: datetime,
    max_date: datetime
):
    logger.info(f'dashboard.py - Processing data for dashboard - [{min_date} to {max_date}]')

    if not is_admin(user, session):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Protected resource'
        )

    total = get_total(session, min_date, max_date)
    donations_per_method = get_donations_per_method(
        session, min_date, max_date
    )
    top10_donors = get_top10_donors(session, min_date, max_date)
    top10_institutions = get_top10_institutions(session, min_date, max_date)
    donations_per_sector = get_donations_per_sector(
        session, min_date, max_date
    )

    return DashboardResponse(
        total=total,
        donations_per_method=donations_per_method,
        top10_donors=top10_donors,
        top10_institutions=top10_institutions,
        donations_per_sector=donations_per_sector
    )
