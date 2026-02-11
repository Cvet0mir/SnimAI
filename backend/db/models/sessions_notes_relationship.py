from sqlalchemy import Table, Column, ForeignKey
from ..database import Base

association_table = Table(
    "sessions_notes",
    Base.metadata,
    Column("session_id", ForeignKey("sessions.id", name="fk_sessions_table"), primary_key=True),
    Column("note_id", ForeignKey("notes.id", name="fk_notes_table"), primary_key=True),
)
