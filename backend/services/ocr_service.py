from ..ml.ocr_model import extract_text

async def run_ocr(image_path: str) -> str:
    text = extract_text(image_path)
    return text
