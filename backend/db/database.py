from typing import Annotated
from datetime import datetime

from sqlalchemy import create_engine, String, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, registry

from core.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

str_100 = Annotated[str, 100]
datetime_tz = Annotated[datetime, "tz"]

class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map = {
            str_100: String(100),
            datetime_tz: DateTime(timezone=True)
        }
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

