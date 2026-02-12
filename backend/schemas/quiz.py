from datetime import datetime

from .orm_base import BaseORM
from .question import QuestionOut


class QuizOut(BaseORM):
    id: int
    session_id: int
    created_at: datetime
    questions: list[QuestionOut]
