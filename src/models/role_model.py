from pydantic import BaseModel, ConfigDict
from enum import Enum


class RoleLevelEnum(Enum):
    USER = 1
    ADMIN = 2


class RoleEnum(Enum):
    USER = 'user'
    ADMIN = 'admin'


class RoleIdEnum(Enum):
    USER = 0
    ADMIN = 1


class Role(BaseModel):
    id: int
    role: RoleEnum = RoleEnum.USER
    level: RoleLevelEnum = RoleLevelEnum.USER
