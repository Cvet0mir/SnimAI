from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base, str_100, datetime_tz

class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = relationship(ForeignKey("users.id"))
    session_id: Mapped[int] = relationship(ForeignKey("sessions.id"))
    image_path: Mapped[str]
    raw_ocr_text: Mapped[str]
    clean_ocr_text: Mapped[str]
    language: Mapped[str_100]
    created_at: Mapped[datetime_tz] = mapped_column(default=func.now())

    # TODO: many-to-one relationships to the summaries, flash cards, quizes and processing jobs

