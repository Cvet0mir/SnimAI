import os
import uuid
from pathlib import Path
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
    Form,
)
from sqlalchemy.orm import Session as DBSession

from ..dependecies import get_db, get_current_user
from ..core.config import settings

from ..db.models.user import User
from ..db.models.note import Note
from ..db.models.session import Session
from ..schemas.note import NoteOut


router = APIRouter(prefix="/notes", tags=["notes"])

UPLOAD_DIR = Path(settings.IMAGE_UPLOAD_DIR)
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
async def create_note(
    image: Annotated[UploadFile, File(...)],
    language: Annotated[str, Form(...)],
    session_id: Annotated[int, Form(...)],
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

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    db: Annotated[DBSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    note = (
        db.query(Note)
        .filter(
            Note.id == note_id,
            Note.user_id == current_user.id,
        )
        .first()
    )

    if not note:
        raise HTTPException(status_code=404, detail="Бележката не намерена")
    if os.path.exists(note.image_path):
        os.remove(note.image_path)

    db.delete(note)
    db.commit()
    return None

