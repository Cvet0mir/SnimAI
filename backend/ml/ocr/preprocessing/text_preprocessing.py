import re

def normalize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" ,", ",").replace(" .", ".")
    return text.strip()

def remove_ocr_artifacts(text: str) -> str:
    text = re.sub(r"[^\w\s,.!?-]", "", text)
    return normalize_text(text)