from typing import Annotated

import os
import uuid
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, File, Form, UploadFile
from sqlalchemy.orm import Session as DBSession

from ..core.config import settings
from ..dependencies import get_db, get_current_user

from ..db.models.user import User
from ..db.models.note import Note
from ..db.models.session import Session
from ..db.models.summary import Summary
from ..db.models.quiz import Quiz
from ..db.models.enums.status_enum import Status

from ..schemas.session import SessionCreate, SessionOut
from ..schemas.note import NoteOut
from ..schemas.summary import SummaryOut
from ..schemas.quiz import QuizOut


router = APIRouter(prefix="/sessions", tags=["sessions"])

UPLOAD_DIR = Path(settings.IMAGE_UPLOAD_DIR)
UPLOAD_DIR.mkdir(exist_ok=True)


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
        raise HTTPException(
            status_code=404, 
            detail="Сесията не е намерена"
        )

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
        raise HTTPException(
            status_code=404, 
            detail="Сесията не е намерена"
        )

    db.delete(session)
    db.commit()

    return None


@router.post("/{session_id}/notes", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
async def create_note(
    session_id: int,
    image: Annotated[UploadFile, File(...)],
    language: Annotated[str, Form(...)],
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

    img_extension = Path(image.filename).suffix
    unique_filename = f"{uuid.uuid4()}{img_extension}"
    file_path = UPLOAD_DIR / unique_filename

    with open(file_path, "wb") as buffer:
        content = await image.read()
        buffer.write(content)

    note = Note(
        user_id=current_user.id,
        image_path=str(file_path),
        raw_ocr_text=None,
        clean_ocr_text=None,
        language=language,
    )
    note.sessions.append(session)

    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@router.delete("/{session_id}/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    session_id: int,
    note_id: int,
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
    note = next(
        filter(lambda x: x.id == note_id, session.notes), 
        None
    )

    if not note:
        raise HTTPException(
            status_code=404, 
            detail="Бележката не намерена"
        )
    if os.path.exists(note.image_path):
        os.remove(note.image_path)

    db.delete(note)
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
        raise HTTPException(
            status_code=404, 
            detail="Сесията не е намерена"
        )

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


@router.get("/{session_id}/summary", response_model=SummaryOut)
def get_session_summary(
    session_id: int,
    db: Annotated[DBSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    session = (
        db.query(Session)
        .filter(
            Session.id == session_id,
            Session.user_id == current_user.id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Сесията не е намерена"
        )

    summary = (
        db.query(Summary)
        .filter(
            Summary.session_id == session_id
        )
        .first()
    )

    if not summary:
        raise HTTPException(
            status_code=404, 
            detail="Обобщението не е намерено"
        )

    return summary


@router.get("/{session_id}/quizzes", response_model=list[QuizOut])
def get_session_quizzes(
    session_id: int,
    db: Annotated[DBSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    session = (
        db.query(Session)
        .filter(
            Session.id == session_id,
            Session.user_id == current_user.id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404, 
            detail="Сесията не е намерена"
        )

    quizzes = (
        db.query(Quiz)
        .filter(
            Quiz.session_id == session_id
        )
        .all()
    )
    return quizzes


@router.get("/{session_id}/quizzes/{quiz_id}", response_model=QuizOut)
def get_session_quiz_by_id(
    session_id: int,
    quiz_id: int,
    db: Annotated[DBSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    quiz = (
        db.query(Quiz)
        .join(Session)
        .filter(
            Quiz.id == quiz_id,
            Quiz.session_id == session_id,
            Session.user_id == current_user.id
        )
        .first()
    )

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Тестът не е намерен"
        )

    return quiz


