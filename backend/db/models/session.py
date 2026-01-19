from sqlalchemy import ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base, str_100, datetime_tz
from enums.status_enum import Status

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str_100] = mapped_column(unique=True)
    status: Mapped[Status] = mapped_column(
        Enum(
            Status,
            name="session_status"
        )
    )
    created_at: Mapped[datetime_tz] = mapped_column(default=func.now())
    finished_at: Mapped[datetime_tz] = mapped_column()
    note_count: Mapped[int]

