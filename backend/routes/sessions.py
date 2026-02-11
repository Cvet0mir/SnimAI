from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DBSession

from ..dependecies import get_db, get_current_user

from ..db.models.user import User
from ..db.models.note import Note
from ..db.models.session import Session
from ..db.models.enums.status_enum import Status

from ..schemas.session import SessionCreate, SessionOut
from ..schemas.note import NoteOut


router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
def create_session(
    session_data: SessionCreate,
    db: Annotated[DBSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    existing = db.query(Session).filter(Session.name == session_data.name).first()
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="Сесия с това име вече съществува. Моля, преименувайте новата"
        )

    session = Session(
        user_id=current_user.id,
        name=session_data.name,
        status=Status(session_data.status),
    )
    db.add(session)

    db.commit()
    db.refresh(session)
    return session


@router.get("/", response_model=list[SessionOut])
def get_sessions(
    db: Annotated[DBSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    sessions = (
        db.query(Session)
        .filter(Session.user_id == current_user.id)
        .order_by(Session.created_at.desc())
        .all()
    )

    return sessions


@router.get("/{session_id}", response_model=SessionOut)
def get_session(
    session_id: int,
    db: Annotated[DBSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    session = (
        db.query(Session)
        .filter(
            Session.id == session_id,
            Session.user_id == current_user.id,
        )
        .first()
    )

    if not session:
        raise HTTPException(status_code=404, detail="Сесията не е намерена")

    return session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: int,
    db: Annotated[DBSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    session = (
        db.query(Session)
        .filter(
            Session.id == session_id,
            Session.user_id == current_user.id,
        )
        .first()
    )

    if not session:
        raise HTTPException(status_code=404, detail="Сесията не е намерена")

    db.delete(session)
    db.commit()

    return None


@router.get("/{session_id}/notes", response_model=list[NoteOut])
def get_session_notes(
    session_id: int,
    db: Annotated[DBSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    session = (
        db.query(Session)
        .filter(
            Session.id == session_id,
            Session.user_id == current_user.id,
        )
        .first()
    )

    if not session:
        raise HTTPException(status_code=404, detail="Сесията не е намерена")

    return session.notes


@router.get("/{session_id}/notes/{note_id}", response_model=NoteOut)
def get_session_note_by_id(
    session_id: int,
    note_id: int,
    db: Annotated[DBSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    note = (
        db.query(Note)
        .join(Note.sessions)
        .filter(
            Note.id == note_id,
            Session.id == session_id,
            Note.user_id == current_user.id,
        )
        .first()
    )

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Тази бележка не е намерена в сесията"
        )

    return note
