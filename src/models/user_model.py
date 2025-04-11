from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class Message(BaseModel):
    message: str

        
class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    avatar_url: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar_url: Optional[str] = None
    role: str
    model_config = ConfigDict(
        from_attributes=True, ser_json_timedelta='iso8601'
    )


class UserDB(User):
    id: int
    role_id: int


class UserResponseList(BaseModel):
    users: list[UserResponse]


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    avatar_url: Optional[str] = None
