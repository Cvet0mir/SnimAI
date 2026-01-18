from typing import Annotated
from pydantic import Field, EmailStr
from orm_base import BaseORM

class UserBase(BaseORM):
    email: EmailStr

class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=8)]

class UserLogin(UserCreate):
    ...

class UserOut(UserBase):
    id: int

class Token(BaseORM):
    access_token: str
    token_type: str
