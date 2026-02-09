from typing import Annotated
from datetime import datetime
from fastapi import UploadFile

from .orm_base import BaseORM

class NoteCreate(BaseORM):
    image_bytes: bytes
    file: UploadFile
    session_id: int

class NoteOut:
    id: int
    session_id: int
    clean_text: str
    created_at: datetime
