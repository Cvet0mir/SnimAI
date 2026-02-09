from typing import Annotated
from datetime import datetime

from sqlalchemy import create_engine, String, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, registry

from backend.core.config import settings

DATABASE_URL = settings.DATABASE_URL

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

str_100 = Annotated[str, 100]
datetime_tz = Annotated[datetime, DateTime(timezone=True)]

class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            str_100: String(100),
            datetime_tz: DateTime(timezone=True)
        }
    )

