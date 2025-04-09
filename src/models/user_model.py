from pydantic import BaseModel, EmailStr, ConfigDict


class Message(BaseModel):
    message: str

        
class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    avatar_url: str
    role_id: int


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar_url: str
    role: str
    model_config = ConfigDict(
        from_attributes=True, ser_json_timedelta='iso8601'
    )


class UserDB(User):
    id: int


class UserResponseList(BaseModel):
    users: list[UserResponse]
