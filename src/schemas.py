from pydantic import BaseModel, EmailStr, Field
from datetime import date


class ContactBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    phone: str
    birthdate: date
    otherinform: str

class ContactUpdate(ContactBase):
    email: EmailStr
    phone: str

class ContactResponse(ContactBase):
    id: int
    class Config:
        orm_mode = True

class UserModel(BaseModel):
    email: str
    password: str = Field(min_length=4, max_length=15)


class UserDb(BaseModel):
    id: int
    email: str
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: str