from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from src.models.exceptions import InvalidFormException
import re


class Donor(BaseModel):
    name: str
    avatar_url: Optional[str] = None
    cpf_cnpj: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        if len(value.strip()) < 3:
            raise InvalidFormException(detail=f'Invalid: {value}')
        return value

    @field_validator('cpf_cnpj')
    @classmethod
    def validate_cpfcnpj(cls, value: str) -> str:
        if not re.fullmatch(r'\d{11}|\d{14}', value):
            raise InvalidFormException(detail=f'Invalid: {value}')
        return value


class DonorResponse(BaseModel):
    id: int
    name: str
    avatar_url: Optional[str] = None
    cpf_cnpj: str
    username: str
    model_config = ConfigDict(
        from_attributes=True, ser_json_timedelta='iso8601'
    )


class DonorDB(Donor):
    id: int
    user_id: int


class DonorResponseList(BaseModel):
    donors: list[DonorResponse]


class DonorUpdate(BaseModel):
    name: Optional[str] = None
    avatar_url: Optional[str] = None
