from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base, str_100, datetime_tz

class Summary(Base):
    __tablename__ = "summaries"

    id: Mapped[int] = mapped_column(primary_key=True)
    note_id: Mapped[int] = relationship(ForeignKey("summaries.id"))
    summary_text: Mapped[str]
    used_model: Mapped[str_100]
    created_at: Mapped[datetime_tz] = mapped_column(default=func.now())

