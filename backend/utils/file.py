import uuid
from pathlib import Path

UPLOAD_DIR = Path("data/uploads")

def save_image(file_bytes: bytes, suffix=".jpg") -> Path:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_name = f"{uuid.uuid4()}{suffix}"
    path = UPLOAD_DIR / file_name
    path.write_bytes(file_bytes)
    return path

