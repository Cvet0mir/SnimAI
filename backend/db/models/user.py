from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base, str_100, datetime_tz
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str_100]
    email: Mapped[str_100] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime_tz] = mapped_column(default=func.now())
    current_streak: Mapped[int] = mapped_column(default=0)
    last_active_date: Mapped[datetime_tz] = mapped_column(nullable=True)

    sessions: Mapped[list["Session"]] = relationship(cascade="all, delete-orphan")
    notes: Mapped[list["Note"]] = relationship(cascade="all, delete-orphan")

