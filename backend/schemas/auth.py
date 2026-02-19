from typing import Optional, Annotated
from pydantic import Field, EmailStr
from .orm_base import BaseORM


class UserBase(BaseORM):
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]
class UserCreate(UserBase):
    name: str

class UserLogin(UserBase):
    ...

class UserUpdate(BaseORM):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[Annotated[str, Field(min_length=8)]] = None

class UserOut(BaseORM):
    id: int
    name: str
    email: str


class Token(BaseORM):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshToken(BaseORM):
    refresh_token: str

