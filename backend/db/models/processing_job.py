from typing import Optional

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base, datetime_tz
from enums.job_types import JobType
from enums.status_enum import Status

class ProcessingJob(Base):
    __tablename__ = "processing_jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[Optional[int]] = relationship(ForeignKey("sessions.id"))
    note_id: Mapped[Optional[int]] = relationship(ForeignKey("notes.id"))
    job_type: Mapped[JobType] = mapped_column(
        Enum(
            JobType,
            name="processing_job_type"
        )
    )
    status: Mapped[Status] = mapped_column(
        Enum(
            Status,
            name="processing_job_status"
        )
    )
    error_message: Mapped[Optional[str]]
    started_at: Mapped[datetime_tz]
    finished_at: Mapped[datetime_tz]
