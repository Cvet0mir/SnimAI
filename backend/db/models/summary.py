from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base, str_100, datetime_tz


class Summary(Base):
    __tablename__ = "summaries"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id", name="fk_summaries_session"))
    summary_text: Mapped[str]
    used_model: Mapped[str_100]
    created_at: Mapped[datetime_tz] = mapped_column(default=func.now())
