from sqlalchemy.orm import Session as DbSession
from ..db.models.session import Session
from ..db.models.enums.status_enum import Status

from ..dependecies import get_db
from ..utils.text import chunk_text

from .ocr_service import run_ocr
from .retrieval_service import add_chunks_to_index, retrieve_relevant
from .summarizing_service import summarize_text
from .quiz_service import create_quiz


def run_processing_pipeline(session_id: int, num_questions: int):
    db: DbSession = get_db()
    try:
        session = db.query(Session).first(Session.id == session_id)
        images = [x.image_path for x in session.notes]

        text = ""
        for img_path in images:
            text += run_ocr(img_path) + "\n"

        chunks = chunk_text(text)
        add_chunks_to_index(chunks)

        chunks = retrieve_relevant("main ideas and key concepts")
        context = "\n\n".join(chunks)
        summary = summarize_text(text)

        chunks = retrieve_relevant("important facts and definitions")
        context = "\n\n".join(chunks)
        quiz = create_quiz(text)

        session.summaries.add(summary)
        session.quizzes.extend(quiz)
        session.status = Status.done
        db.commit()
        db.refresh()

    except Exception as exc:
        session.status = Status.failed
        raise RuntimeError("Не успяхме да обработим заявката ви. Моля, опитайте отново")

