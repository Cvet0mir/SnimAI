from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base, str_100, datetime_tz
from summary import Summary
from flashcard import Flashcard
from quiz import Quiz
from processing_job import ProcessingJob


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))

    image_path: Mapped[str]
    raw_ocr_text: Mapped[str]
    clean_ocr_text: Mapped[str]
    language: Mapped[str_100]
    created_at: Mapped[datetime_tz] = mapped_column(default=func.now())

    summaries: Mapped[list[Summary]] = relationship()
    flashcards: Mapped[list[Flashcard]] = relationship()
    quizzes: Mapped[list[Quiz]] = relationship()
    processing_jobs: Mapped[list[ProcessingJob]] = relationship()
