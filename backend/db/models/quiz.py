from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base, datetime_tz


class Quiz(Base):
    __tablename__ = "quizzes"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id", name="fk_quizzes_session"))
    created_at: Mapped[datetime_tz] = mapped_column(default=func.now())

    session: Mapped["Session"] = relationship(back_populates="quizzes")
    questions: Mapped[list["Question"]] = relationship("Question", back_populates="quiz")
