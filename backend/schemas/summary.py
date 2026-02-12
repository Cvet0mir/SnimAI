from datetime import datetime
from typing import Annotated
from pydantic import Field

from .orm_base import BaseORM


class SummaryOut(BaseORM):
    id: int
    session_id: int
    summary_text: str
    used_model: Annotated[str, Field(max_length=100)]
    created_at: datetime
