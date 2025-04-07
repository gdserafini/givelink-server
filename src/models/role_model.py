from pydantic import BaseModel, ConfigDict
from enum import Enum


class RoleLevelEnum(Enum):
    USER = 1
    ADMIM = 2


class RoleEnum(Enum):
    USER = 'user'
    ADMIN = 'admin'


class Role(BaseModel):
    id: int
    role: RoleEnum = RoleEnum.USER
    level: RoleLevelEnum = RoleLevelEnum.USER
