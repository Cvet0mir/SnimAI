from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session as DBSession

from ..schemas.session import SessionOut
from ..db.models.user import User, Session
from ..db.models.enums.status_enum import Status
from ..dependencies import get_current_user, get_db

from ..services.processing_pipeline import run_processing_pipeline

router = APIRouter(prefix="/processing", tags=["processing"])

@router.post("/start/{session_id}", status_code=status.HTTP_202_ACCEPTED)
def start_processing(
    session_id: int,
    background_tasks: BackgroundTasks,
    db: Annotated[DBSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    session = db.query(Session).filter(Session.id == session_id).first()

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


@router.get("/status/{session_id}")
def get_status(
    session_id: int,
    db: Annotated[DBSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    session = db.query(Session).filter(Session.id == session_id).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сесията не е намерена"
        )

    return {
        "session_id": session.id,
        "status": session.status.value,
        "created_at": session.created_at,
        "finished_at": session.finished_at
    }


@router.get("/result/{session_id}", response_model=SessionOut)
def get_result(
    session_id: int,
    db: Annotated[DBSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    session = db.query(Session).filter(Session.id == session_id).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сесията не е намерена"
        )
    if session.status != Status.done:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Обработването не е завършило"
        )

    return session


