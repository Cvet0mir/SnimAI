from .orm_base import BaseORM

class QuizBase(BaseORM):
    note_id: int
    question: str
    options: list[str]
    correct_answer: str

class QuizCreate(QuizBase):
    ...

class QuizOut(QuizBase):
    id: int
