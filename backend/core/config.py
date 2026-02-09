import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    EMBEDDINGS_MODEL_PATH: str = os.getenv("EMBEDDINGS_MODEL_PATH")

    LLM_MODEL_PATH: str = os.getenv("LLAMA_MODEL_ID")
    MAX_TOKENS: str = os.getenv("MAX_TOKENS")

    DATABASE_URL: str = os.getenv("DATABASE_URL")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60))

    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", 30))


settings = Settings()
