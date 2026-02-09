from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base, str_100, datetime_tz
from .session import Session
from .note import Note


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str_100]
    email: Mapped[str_100] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime_tz] = mapped_column(default=func.now())

    sessions: Mapped[list[Session]] = relationship()
    notes: Mapped[list[Note]] = relationship()
