from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_create_enums"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    session_status_enum = sa.Enum(
        "PENDING", "RUNNING", "FINISHED", "FAILED",
        name="session_status"
    )
    processing_job_status_enum = sa.Enum(
        "PENDING", "RUNNING", "FINISHED", "FAILED",
        name="processing_job_status"
    )
    processing_job_type_enum = sa.Enum(
        "OCR", "SUMMARY", "FLASHCARD", "QUIZ",
        name="processing_job_type"
    )

    session_status_enum.create(op.get_bind(), checkfirst=True)
    processing_job_status_enum.create(op.get_bind(), checkfirst=True)
    processing_job_type_enum.create(op.get_bind(), checkfirst=True)


def downgrade():
    sa.Enum(name="session_status").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="processing_job_status").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="processing_job_type").drop(op.get_bind(), checkfirst=True)
