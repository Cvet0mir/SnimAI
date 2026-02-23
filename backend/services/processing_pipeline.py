from pathlib import Path

from sqlalchemy.orm import Session as DBSession
from ..db.models.session import Session
from ..db.models.enums.status_enum import Status

from ..dependencies import get_db
from ..core.config import settings
from ..utils.text import chunk_text

from .ocr_service import OCRService
from .retrieval_service import RetrievalService
from .summarizing_service import summarize_text
from .quiz_service import create_quiz

ocr_service = OCRService()
retrieval_service = RetrievalService()

UPLOAD_DIR = Path(settings.IMAGE_UPLOAD_DIR)
UPLOAD_DIR.mkdir(exist_ok=True)

def run_processing_pipeline(session_id: int, num_questions: int):
    db: DBSession = next(get_db())
    session = None
    try:
        session = db.query(Session).filter(Session.id == session_id).first()
        if not session:
            raise ValueError(f"Session {session_id} not found")

        print("Entered the pipe line")
        retrieval_service.reset_session(session_id)
        print("Done with the retrieval")

        images = [x.image_path for x in session.notes]
        full_text = ""
        for note in session.notes:
            img_path = UPLOAD_DIR / Path(note.image_path).name
            recognized_text = ocr_service.extract_text(str(img_path))
            full_text += recognized_text + "\n"
        print("Extracted the text")

        chunks = chunk_text(full_text)
        for chunk in chunks:
            retrieval_service.index_text(session_id, chunk)
        print("Chunked it")

        main_ideas = retrieval_service.retrieve_chunks(session_id, "main ideas and key concepts")
        context_main = "\n\n".join(main_ideas)
        summary = summarize_text(context_main)
        print("Summarized it")

        facts = retrieval_service.retrieve_chunks(session_id, "important facts and definitions")
        context_facts = "\n\n".join(facts)
        quiz = create_quiz(context_facts, num_questions=num_questions)
        print("Made tests")

        session.summaries.append(summary)
        session.quizzes.extend(quiz)
        session.status = Status.finished.value
        print("extended it")

        db.commit()
        db.refresh(session)
        print("refreshed it")

    except Exception as exc:
        print("or not so much")
        if session:
            session.status = Status.failed.value
            db.commit()
        raise RuntimeError(
            "Не успяхме да обработим заявката ви. Моля, опитайте отново"
        ) from exc
    

