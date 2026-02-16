from sqlalchemy.orm import Session as DBSession
from ..db.models.session import Session
from ..db.models.enums.status_enum import Status

from ..dependencies import get_db
from ..utils.text import chunk_text

from .ocr_service import OCRService
from .retrieval_service import RetrievalService
from .summarizing_service import summarize_text
from .quiz_service import create_quiz

ocr_service = OCRService()
retrieval_service = RetrievalService()


def run_processing_pipeline(session_id: int, num_questions: int):
    db: DBSession = get_db()
    try:
        session = db.query(Session).filter(Session.id == session_id).first()
        if not session:
            raise ValueError(f"Session {session_id} not found")

        retrieval_service.reset_session(session_id)

        images = [x.image_path for x in session.notes]
        full_text = ""
        for img_path in images:
            recognized_text = ocr_service.extract_text(img_path)
            full_text += recognized_text + "\n"

        chunks = chunk_text(full_text)
        for chunk in chunks:
            retrieval_service.index_text(session_id, chunk)

        main_ideas = retrieval_service.retrieve_chunks(session_id, "main ideas and key concepts")
        context_main = "\n\n".join(main_ideas)
        summary = summarize_text(context_main)

        facts = retrieval_service.retrieve_chunks(session_id, "important facts and definitions")
        context_facts = "\n\n".join(facts)
        quiz = create_quiz(context_facts, num_questions=num_questions)

        session.summaries.append(summary)
        session.quizzes.extend(quiz)
        session.status = Status.done

        db.commit()
        db.refresh(session)

    except Exception as exc:
        if session:
            session.status = Status.failed
            db.commit()
        raise RuntimeError(
            "Не успяхме да обработим заявката ви. Моля, опитайте отново"
        ) from exc
