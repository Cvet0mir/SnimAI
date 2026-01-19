from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision = "0002_create_tables"
down_revision = "0001_create_enums"
branch_labels = None
depends_on = None


def upgrade():
    session_status_enum = ENUM(
        "PENDING", "RUNNING", "FINISHED", "FAILED",
        name="session_status",
        create_type=False
    )

    processing_job_status_enum = ENUM(
        "PENDING", "RUNNING", "FINISHED", "FAILED",
        name="processing_job_status",
        create_type=False
    )

    processing_job_type_enum = ENUM(
        "OCR", "SUMMARY", "FLASHCARD", "QUIZ",
        name="processing_job_type",
        create_type=False
    )

    # ---- USERS ----
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(100), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ---- SESSIONS ----
    op.create_table(
        "sessions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(100), nullable=False, unique=True),
        sa.Column("status", session_status_enum, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("note_count", sa.Integer, nullable=False),
    )

    # ---- NOTES ----
    op.create_table(
        "notes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("session_id", sa.Integer, sa.ForeignKey("sessions.id"), nullable=False),
        sa.Column("image_path", sa.String, nullable=False),
        sa.Column("raw_ocr_text", sa.Text, nullable=False),
        sa.Column("clean_ocr_text", sa.Text, nullable=False),
        sa.Column("language", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ---- SUMMARIES ----
    op.create_table(
        "summaries",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("note_id", sa.Integer, sa.ForeignKey("notes.id"), nullable=False),
        sa.Column("summary_text", sa.Text, nullable=False),
        sa.Column("used_model", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ---- FLASHCARDS ----
    op.create_table(
        "flashcards",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("note_id", sa.Integer, sa.ForeignKey("notes.id"), nullable=False),
        sa.Column("question", sa.Text, nullable=False),
        sa.Column("answer", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ---- QUIZZES ----
    op.create_table(
        "quizzes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("note_id", sa.Integer, sa.ForeignKey("notes.id"), nullable=False),
        sa.Column("question", sa.Text, nullable=False),
        sa.Column("options", sa.Text, nullable=False),
        sa.Column("correct_answer", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ---- PROCESSING JOBS ----
    op.create_table(
        "processing_jobs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("session_id", sa.Integer, sa.ForeignKey("sessions.id"), nullable=True),
        sa.Column("note_id", sa.Integer, sa.ForeignKey("notes.id"), nullable=True),
        sa.Column("job_type", processing_job_type_enum, nullable=False),
        sa.Column("status", processing_job_status_enum, nullable=False),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade():
    op.drop_table("processing_jobs")
    op.drop_table("quizzes")
    op.drop_table("flashcards")
    op.drop_table("summaries")
    op.drop_table("notes")
    op.drop_table("sessions")
    op.drop_table("users")
