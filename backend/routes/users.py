from fastapi import HTTPException, status, Depends, APIRouter

from ..db.models.user import User
from ..dependecies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def update_profile(current_user: User = Depends(get_current_user)):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Profile updating not implemented yet"
    )

@router.delete("/me", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def delete_profile(current_user: User = Depends(get_current_user)):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Profile updating not implemented yet"
    )


