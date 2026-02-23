from typing import Optional

from .orm_base import BaseORM


class QuestionBase(BaseORM):
    question: str
    options: Optional[list[str]] = None
    correct_answer: str


class QuestionOut(QuestionBase):
    id: int
