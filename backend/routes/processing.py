from fastapi import APIRouter, Depends, status, HTTPException

from ..db.models.user import User
from ..dependecies import get_current_user

router = APIRouter(prefix="/processing", tags=["processing"])

@router.post("/start/{session_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def start_processing(session_id: int, current_user: User = Depends(get_current_user)):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Starting the processing for a session not implemented yet"
    )

@router.get("/status/{session_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def get_status(session_id: int, current_user: User = Depends(get_current_user)):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Getting the status of the processing for a session not implemented yet"
    )

@router.get("/result/{session_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def get_result(session_id: int, current_user: User = Depends(get_current_user)):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Getting the result from the processing for a session not implemented yet"
    )


