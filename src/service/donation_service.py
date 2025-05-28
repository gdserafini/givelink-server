from src.models.donation_model import Donation, DonationResponse
from sqlalchemy.orm import Session
from src.models.db_schemas import DonationModel, DonorModel, InstitutionModel, UserModel
from sqlalchemy import select
from src.models.user_model import User, Message
from fastapi import HTTPException
from http import HTTPStatus
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from src.utils.logging import logger


TAX = 0.04
FEES = 0.0199


def generate_contract(donation: DonationResponse) -> None:
    contract_text = f"""
    Este contrato firma a doação de ID {donation.id} entre o doador: {donation.donor} 
    e a instituição {donation.institution} na data de {donation.date}. 
    O valor doador é de R$ {donation.amount} pago via {donation.payment_method}

    Assinaturas
    {donation.donor}
    ---------------------    
    {donation.institution}
    ---------------------"""
    canvas = Canvas(f'contracts/contract_{donation.id}.pdf', pagesize=A4)
    text_object = canvas.beginText()
    text_object.setTextOrigin(100, 750)
    text_object.setFont('Helvetica', 12)
    for line in contract_text.split('\n'):
        text_object.textLine(line)
    canvas.drawText(text_object)
    canvas.save()
    #TODO -> Send to AWS S3
    logger.info('Report successfully created and saved')
    return


def collect_fees(donation_value: float) -> float:
    if donation_value <= 0 or type(donation_value) != float:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Invalid donation value: {donation_value}'
        )
    logger.info('Fees collected')
    return donation_value * (1-(TAX + FEES))


def generate_invoice(donation: DonationResponse) -> None:
    invoice_text = f"""
    Nota nº: {donation.id}
    Doador: {donation.donor}
    Instituição: {donation.institution}
    {donation.date}
    Valor: R$ {donation.amount}
    Impostos: R$ {donation.amount * TAX} (4%)
    Taxas GiveLink: R$ {(donation.amount * FEES):.2f} (1,99%)"""
    canvas = Canvas(f'invoices/invoice_{donation.id}.pdf', pagesize=A4)
    text_object = canvas.beginText()
    text_object.setTextOrigin(100, 750)
    text_object.setFont('Helvetica', 12)
    for line in invoice_text.split('\n'):
        text_object.textLine(line)
    canvas.drawText(text_object)
    canvas.save()
    #TODO -> Send to AWS S3
    logger.info('Invoice successfully created and saved')
    return


def get_contract(donation_id: int) -> Canvas:
    #TODO -> Get contract from AWS S3
    ...


def get_invoice(donation_id: int) -> Canvas:
    #TODO -> Get invoice from AWS S3
    ...


def create_donation_service(
    donation: Donation,
    session: Session,
    user: User
) -> DonationResponse:
    donor = session.scalar(
        select(DonorModel).where(
            DonorModel.id == donation.donor_id
        )
    )
    if user.id != donor.user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=f"Logged user and donor's user is different."
        )
    institution = session.scalar(
        select(InstitutionModel).where(
            InstitutionModel.id == donation.institution_id
        )
    )
    donation_amount = collect_fees(donation.amount)
    donation_db = DonationModel(
        amount = donation_amount,
        payment_method = donation.payment_method,
        donor_id = donation.donor_id,
        institution_id = donation.institution_id
    )
    session.add(donation_db)
    session.commit()
    session.refresh(donation_db)
    donation_response = DonationResponse(
        id = donation_db.id,
        amount = donation.amount,
        payment_method = donation.payment_method,
        date = donation_db.date,
        donor = donor.name,
        institution = institution.name
    )
    logger.info('Donation successfully created')
    generate_contract(donation_response)
    generate_invoice(donation_response)
    return donation_response


def get_donations_service(
    user_id: int,
    institution_id: int,
    session: Session,
    offset: int,
    limit: int,
    max_amount: float = None,
    min_amount: float = None,
    min_date: int = None,
    max_date: int = None,
    payment_method: str = None
) -> list[DonationResponse]:
    if offset < 0 or limit < 0 or \
        type(offset) != int or type(limit) != int:
        raise ValueError('Invalid params.')
    user = session.scalar(
            select(UserModel).where(
                UserModel.id == user_id
            )
        )
    if user.username == 'admin':
        query = select(DonationModel)
    else:
        institution = session.scalar(
            select(InstitutionModel).where(
                InstitutionModel.id == institution_id
            )
        )
        if institution.user_id != user_id:
            raise HTTPException(
                status_code=HTTPStatus.Forbidden,
                detail='User not allowed to access this resource.'
            )
        query = select(DonationModel).where(
            DonationModel.institution_id == institution_id
        )
    if min_amount is not None:
        query = query.where(DonationModel.amount >= min_amount)
    if max_amount is not None:
        query = query.where(DonationModel.amount <= max_amount)
    if min_date is not None:
        query = query.where(DonationModel.date >= min_date)
    if max_date is not None:
        query = query.where(DonationModel.date <= max_date)
    if payment_method is not None:
        query = query.where(DonationModel.payment_method == payment_method)
    query = query.offset(offset).limit(limit)
    donations = session.scalars(query).all()
    logger.info('Donation successfully found by filters')
    return [
        cast_to_donation_response(donation, session) 
        for donation in donations 
    ]


def cast_to_donation_response(
    donation: Donation, 
    session: Session
) -> DonationResponse:
    donor = session.scalar(
        select(DonorModel).where(
            DonorModel.id == donation.donor_id
        )
    )
    institution = session.scalar(
        select(InstitutionModel).where(
            InstitutionModel.id == donation.institution_id
        )
    )
    return DonationResponse(
        id=donation.id,
        amount=donation.amount,
        date=donation.date,
        payment_method=donation.payment_method,
        institution=institution.name,
        donor=donor.name
    )


def get_donation_by_id_service(
    session: Session, 
    donation_id: int,
    cast: bool = True
) -> DonationResponse:
    donation = session.scalar(
        select(DonationModel).where(
            DonationModel.id == donation_id
        )
    )
    if not donation:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Donation {donation_id} not found.'
        )
    logger.info('Donation successfully found by id')
    if cast: return cast_to_donation_response(donation, session)
    else: return donation  


def delete_donation_by_id_service(
    id: int, 
    session: Session
) -> Message:
    donation = get_donation_by_id_service(session, id, False)
    session.delete(donation)
    session.commit()
    logger.info('Donation successfully deleted')
    return Message(
        message=f'Donation: {id} deleted successfuly.'
    )