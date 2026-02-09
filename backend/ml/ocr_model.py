from paddleocr import PaddleOCR
from ..core.config import settings

ocr_model = PaddleOCR(
    use_angle_cls=True,
    rec_model_dir=settings.HANDWRITING_MODEL_PATH,
    rec_char_type='en',  # will be chnaged to a bulgarian alphabet later
    lang='en',   # will be changed later
)

def extract_text(image_path: str):
    results = ocr_model.predict(image_path, cls=True)
    text_lines = [line[1][0] for line in results[0]]
    return "\n".join(text_lines)

