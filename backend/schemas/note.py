from datetime import datetime
from fastapi import UploadFile

from .orm_base import BaseORM

class NoteCreate(BaseORM):
    file: UploadFile
    language: str
    session_id: int

class NoteOut(BaseORM):
    id: int
    image_path: str
    raw_ocr_text: str | None
    clean_ocr_text: str | None
    language: str
    created_at: datetime
