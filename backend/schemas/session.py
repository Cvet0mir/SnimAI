from typing import Annotated, Optional, Literal
from datetime import datetime
from pydantic import Field

from .orm_base import BaseORM

class SessionBase(BaseORM):
    name: Annotated[str, Field(max_length=125)]

class SessionCreate(SessionBase):
    status: Literal["pending", "running", "done", "failed"]

class SessionOut(SessionBase):
    id: int
    user_id: int
    status: Literal["pending", "running", "done", "failed"]
    created_at: datetime
    finished_at: Optional[datetime]
