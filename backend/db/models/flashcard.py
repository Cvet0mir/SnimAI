from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base, datetime_tz

class Flashcard(Base):
    __tablename__ = "flashcards"

    id: Mapped[int] = mapped_column(primary_key=True)
    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id"))
    question: Mapped[str]
    answer: Mapped[str]
    created_at: Mapped[datetime_tz] = mapped_column(default=func.now())

