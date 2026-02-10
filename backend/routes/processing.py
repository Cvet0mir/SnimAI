from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session as DbSession

from ..db.models.user import User, Session
from ..db.models.enums.status_enum import Status
from ..dependecies import get_current_user, get_db

from ..services.processing_pipeline import run_processing_pipeline

router = APIRouter(prefix="/processing", tags=["processing"])

@router.post("/start/{session_id}", status_code=status.HTTP_202_ACCEPTED)
def start_processing(
    session_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user), 
    db: DbSession = Depends(get_db)
):
    session = db.query(Session).first(Session.id == session_id)

    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Не можете да посещавате сесия на друг потребител"
        )
    if session.status != Status.pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Тази сесия вече се обработва"
        )
    
    session.status = Status.running
    background_tasks.add_task(run_processing_pipeline, session_id)

    return {"message": "Обработването започна"}


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


