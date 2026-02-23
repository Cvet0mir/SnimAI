from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os

from .routes.auth import router as auth_router
from .routes.notes import router as notes_router
from .routes.processing import router as processing_router
from .routes.sessions import router as sessions_router
from .routes.users import router as users_router

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "uploads"


def create_app() -> FastAPI:
    environment = os.getenv("ENVIRONMENT", "development")

    app = FastAPI(
        title="SnimAI API",
        docs_url="/docs" if environment != "production" else None,
        redoc_url=None if environment == "production" else "/redoc",
    )

    if environment == "production":
        allow_origins = ["*"]
    else:
        allow_origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount(
        "/uploads",
        StaticFiles(directory=str(UPLOAD_DIR)),
        name="uploads",
    )

    api_v1 = APIRouter(prefix="/api/v1")

    api_v1.include_router(auth_router)
    api_v1.include_router(notes_router)
    api_v1.include_router(processing_router)
    api_v1.include_router(sessions_router)
    api_v1.include_router(users_router)

    app.include_router(api_v1)

    return app


app = create_app()

