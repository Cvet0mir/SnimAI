import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    IMAGE_UPLOAD_DIR: str = os.getenv("IMAGE_UPLOAD_DIR")

    HANDWRITING_MODEL_PATH: str = os.getenv("HANDWRITING_MODEL_PATH")

    EMBEDDINGS_MODEL_PATH: str = os.getenv("EMBEDDINGS_MODEL_PATH")
    EMBEDDINGS_DATA_PATH: str = os.getenv("EMBEDDINGS_DATA_PATH")

    CHUNK_SIZE: str = os.getenv("CHUNK_SIZE")
    TOP_K: str = os.getenv("TOP_K")

    LLM_MODEL_PATH: str = os.getenv("LLAMA_MODEL_ID")
    MAX_TOKENS: str = os.getenv("MAX_TOKENS")

    DATABASE_URL: str = os.getenv("DATABASE_URL")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60))

    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", 30))


settings = Settings()
