from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from src.models.exceptions import InvalidFormException


class Donation(BaseModel):
    amount: float
    payment_method: str
    institution_id: int
    donor_id: int

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, value: float) -> float:
        if(value < 0.01):
            raise InvalidFormException(
                detail=f'Invalid: amount: {value}.'
            )
        return value


class DonationResponse(BaseModel):
    id: int
    amount: float
    date: datetime
    payment_method: str
    institution: str
    donor: str
    model_config = ConfigDict(
        from_attributes=True,
        ser_json_timedelta='iso8601'
    )


class DonationDB(Donation):
    id: int


class DonationResponseList(BaseModel):
    donations: list[DonationResponse]
