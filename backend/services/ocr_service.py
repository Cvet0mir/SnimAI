import os
os.environ["FLAGS_use_mkldnn"] = "0"

import cv2
from paddleocr import PaddleOCR

class OCRService:
    def __init__(self, lang: str = "bg"):
        self.ocr = PaddleOCR(
            lang=lang,
            use_textline_orientation=True,
            enable_mkldnn=False,
        )

    def extract_text(self, img_path: str) -> str:
        print(f"[OCRService] Processing {img_path}")
        img = cv2.imread(img_path)
        if img is None:
            raise FileNotFoundError(f"Image not found: {img_path}")

        # Directly predict
        result = self.ocr.predict(img)
        lines = []

        for page in result:
            rec_texts = page.get("rec_texts", [])
            rec_scores = page.get("rec_scores", [])
            for text, score in zip(rec_texts, rec_scores):
                print(f"Detected: {text}, confidence: {score:.3f}")
                if score >= 0.2:
                    lines.append(text.strip())

        return "\n".join(lines)


# Example quick test
if __name__ == "__main__":
    ocr_service = OCRService()
    text = ocr_service.extract_text("C:/Цветомир/Programming/Projects/SnimAI/data/uploads/4c8ad801-5b3c-4c03-be63-19b74bce732f.jpg")
    print("=== OCR Result ===")
    print(text)
