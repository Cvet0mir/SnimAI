from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base, str_100, datetime_tz
from .session import Session
from .sessions_notes_relationship import association_table


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    image_path: Mapped[str]
    raw_ocr_text: Mapped[str | None]
    clean_ocr_text: Mapped[str | None]
    language: Mapped[str_100]
    created_at: Mapped[datetime_tz] = mapped_column(default=func.now())

    sessions: Mapped[list[Session]] = relationship(
        secondary=association_table, back_populates="notes"
    )
