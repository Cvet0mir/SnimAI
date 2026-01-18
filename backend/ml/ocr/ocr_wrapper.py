from paddleocr import PaddleOCR
import numpy as np
from PIL import Image
from preprocessing import image_preprocessing as img_prep
from ocr.preprocessing import text_preprocessing as txt_prep

class OCRWrapper:
    def __init__(self, det_model_dir: str, rec_model_dir: str, use_angle_cls: bool = True, lang: str = "bg") -> None:
        self.ocr = PaddleOCR(
            det_model_dir=det_model_dir,
            rec_model_dir=rec_model_dir,
            use_angle_cls=use_angle_cls,
            lang=lang
        )

    def preprocess_image(self, image: Image.Image) -> Image.Image:
        image = img_prep.resize_image(image)
        image = img_prep.to_grayscale(image)
        image = img_prep.denoise(image)
        return image

    def run_model(self, image_path: str):
        image = Image.open(image_path).convert("RGB")
        preprocessed = self.preprocess_image(image)

        result = self.ocr.predict(np.array(preprocessed), cls=True)

        texts = []
        for line in result[0]:
            _, (text, score) = line
            clean_text = txt_prep.remove_ocr_artifacts(text)
            texts.append({"text": clean_text, "score": score})

        return texts

    def extract_text(self, image_path: str) -> str:
        ocr_results = self.run_model(image_path)
        return "\n".join([r["text"] for r in ocr_results])

