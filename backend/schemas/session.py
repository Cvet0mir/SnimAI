from typing import Annotated, Optional
from datetime import datetime

from pydantic import Field
from orm_base import BaseORM

class SessionCreate(BaseORM):
    name: Annotated[str, Field(max_length=125)]

class SessionOut(BaseORM):
    id: int
    user_id: int
    status: str
    created_at: datetime
    finished_at: Optional[datetime]
    
