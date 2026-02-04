from fastapi import APIRouter, Depends, HTTPException, status

from ..db.models.user import User
from ..dependecies import get_current_user

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def create_session(current_user: User = Depends(get_current_user)):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Session creation not implemented yet"
    )

@router.get("/", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def get_sessions(current_user: User = Depends(get_current_user)):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Session retrieval not implemented yet"
    )

@router.get("/{session_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def get_session(session_id: int, current_user: User = Depends(get_current_user)):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Session retrieval by id not implemented yet"
    )

@router.delete("/{session_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def delete_session(session_id: int, current_user: User = Depends(get_current_user)):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Session removal by id not implemented yet"
    )
