from datetime import datetime
from .orm_base import BaseORM

class SessionOut(BaseORM):
    note_id: int
    summary_text: str
    model_used: str

