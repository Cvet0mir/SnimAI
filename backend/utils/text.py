import re

def normalize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" ,", ",").replace(" .", ".")
    return text.strip()
