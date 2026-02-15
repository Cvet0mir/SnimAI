from typing import Optional, Annotated
from pydantic import Field, EmailStr
from .orm_base import BaseORM


class UserBase(BaseORM):
    name: str
    email: EmailStr
class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=8)]

class UserLogin(UserCreate):
    ...

class UserUpdate(BaseORM):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[Annotated[str, Field(min_length=8)]] = None

class UserOut(UserBase):
    id: int


class Token(BaseORM):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshToken(BaseORM):
    refresh_token: str

