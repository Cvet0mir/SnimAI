from sqlalchemy import ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base, str_100, datetime_tz
from .sessions_notes_relationship import association_table

from .enums.status_enum import Status


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", name="fk_sessions_user"))
    name: Mapped[str_100] = mapped_column(unique=True)
    status: Mapped[Status] = mapped_column(
        Enum(
            Status, 
            name="session_status",
            create_type=False
        )
    )
    created_at: Mapped[datetime_tz] = mapped_column(default=func.now())
    finished_at: Mapped[datetime_tz | None] = mapped_column(nullable=True)

    notes: Mapped[list["Note"]] = relationship(
        "Note",
        secondary=association_table, 
        back_populates="sessions"
    )
    summaries: Mapped[list["Summary"]] = relationship()
    flashcards: Mapped[list["Flashcard"]] = relationship()
    quizzes: Mapped[list["Quiz"]] = relationship()
    processing_jobs: Mapped[list["ProcessingJob"]] = relationship()
