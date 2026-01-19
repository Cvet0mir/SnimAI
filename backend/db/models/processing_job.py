from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base, datetime_tz
from enums.job_types import JobType
from enums.status_enum import Status


class ProcessingJob(Base):
    __tablename__ = "processing_jobs"

    id: Mapped[int] = mapped_column(primary_key=True)

    session_id: Mapped[int | None] = mapped_column(
        ForeignKey("sessions.id"),
        nullable=True
    )
    note_id: Mapped[int | None] = mapped_column(
        ForeignKey("notes.id"),
        nullable=True
    )

    job_type: Mapped[JobType] = mapped_column(
        Enum(
            JobType, 
            name="processing_job_type",
            create_type=False
        )
    )
    status: Mapped[Status] = mapped_column(
        Enum(
            Status, 
            name="processing_job_status",
            create_type=False
        )
    )

    error_message: Mapped[str | None] = mapped_column(nullable=True)
    started_at: Mapped[datetime_tz]
    finished_at: Mapped[datetime_tz | None] = mapped_column(nullable=True)
