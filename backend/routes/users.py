from typing import Annotated

from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session as DBSession

from ..db.models.user import User
from ..schemas.auth import UserOut, UserUpdate
from ..dependencies import get_current_user, get_db
from ..core.security import hash_password

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.patch("/me", response_model=UserOut)
def update_profile(
    user_update: UserUpdate,
    db: Annotated[DBSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    if user_update.name is not None:
        current_user.name = user_update.name

    if user_update.email is not None:
        existing_user = (
            db.query(User)
            .filter(
                User.email == user_update.email,
                User.id != current_user.id
            )
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Този имейл вече е регистриран"
            )
        current_user.email = user_update.email

    if user_update.password is not None:
        current_user.hashed_password = hash_password(user_update.password)

    db.commit()
    db.refresh(current_user)

    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(
    db: Annotated[DBSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    db.delete(current_user)
    db.commit()

    return None

