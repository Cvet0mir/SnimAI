from typing import Optional, Literal
from datetime import datetime

from orm_base import BaseORM

class ProcessingJobBase(BaseORM):
    id: int
    status: Literal["pending", "running", "done", "failed"]

class ProcesingJobOut(ProcessingJobBase):
    job_type: Literal["ocr", "summary", "flashcards", "quiz", "graph"]
    error_message: Optional[str]
    started_at: datetime
    finished_at: datetime

class ProcessingJobStatusOut(ProcessingJobBase):
    ...

