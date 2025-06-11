from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from src.models.exceptions import InvalidFormException
import re


class Institution(BaseModel):
    name: str
    sector: str
    avatar_url: Optional[str] = None
    cnpj: str
    description: Optional[str] = None

    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        if len(value.strip()) < 3:
            raise InvalidFormException(detail=f'Invalid: {value}')
        return value

    @field_validator('cnpj')
    @classmethod
    def validate_cnpj(cls, value: str) -> str:
        if not re.fullmatch(r'\d{14}', value):
            raise InvalidFormException(detail=f'Invalid: {value}')
        return value


class InstitutionResponse(BaseModel):
    id: int
    name: str
    sector: str
    avatar_url: Optional[str] = None
    cnpj: str
    username: str
    description: Optional[str] = None
    model_config = ConfigDict(
        from_attributes=True, ser_json_timedelta='iso8601'
    )


class DonorDB(Institution):
    id: int
    user_id: int


class InstitutionResponseList(BaseModel):
    institutions: list[InstitutionResponse]


class InstitutionUpdate(BaseModel):
    name: Optional[str] = None
    sector: Optional[str] = None
    avatar_url: Optional[str] = None
    description: Optional[str] = None

    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        if len(value.strip()) < 3:
            raise InvalidFormException(detail=f'Invalid: {value}')
        return value
