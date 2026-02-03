from sqlalchemy.orm import Session
from crud.user import UserCrud
from core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)

class AuthService:

    @staticmethod
    def register(db: Session, email: str, password: str):
        if UserCrud.get_by_email(db, email):
            raise ValueError("Email already registered")

        return UserCrud.create(
            db,
            email=email,
            hashed_password=hash_password(password)
        )

    @staticmethod
    def login(db: Session, email: str, password: str):
        user = UserCrud.get_by_email(db, email)

        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        return {
            "access_token": create_access_token(user.id),
            "refresh_token": create_refresh_token(user.id),
        }
