from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class QuizQuestion(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id", name="fk_questions_quiz"))
    question: Mapped[str]
    correct_answer: Mapped[str]

    quiz: Mapped["Quiz"] = relationship(back_populates="questions")
