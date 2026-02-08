from fastapi import FastAPI, APIRouter

from routes.auth import router as auth_router
from routes.notes import router as notes_router
from routes.processing import router as processing_router
from routes.sessions import router as sessions_router
from routes.users import router as users_router


def create_app() -> FastAPI:

    app = FastAPI(title="SnimAI API", docs_url="/docs")
    api_v1 = APIRouter(prefix="/api/v1")

    api_v1.include_router(auth_router)
    api_v1.include_router(notes_router)
    api_v1.include_router(processing_router)
    api_v1.include_router(sessions_router)
    api_v1.include_router(users_router)

    app.include_router(api_v1)
    return app


app = create_app()
