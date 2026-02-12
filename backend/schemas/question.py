from .orm_base import BaseORM


class QuestionBase(BaseORM):
    question: str
    options: list[str]
    correct_answer: str


class QuestionOut(QuestionBase):
    id: int
