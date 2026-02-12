from .orm_base import BaseORM

class FlashcardBase(BaseORM):
    session_id: int
    question: str
    answer: str

class FlahscardCreate(FlashcardBase):
    ...

class FlashcardOut(FlashcardBase):
    id: int

