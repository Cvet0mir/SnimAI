import cv2
import numpy as np
from paddleocr import PaddleOCR

class OCRService:
    def __init__(self, lang: str = "bg", preprocess: bool = True):
        self.ocr = PaddleOCR(lang=lang, use_textline_orientation=True)
        self.preprocess = preprocess

    @staticmethod
    def load_and_preprocess(img_path: str) -> np.ndarray:
        img = cv2.imread(img_path)
        if img is None:
            raise FileNotFoundError(f"Image not found: {img_path}")
        print(f"[Preprocess] Image loaded: {img.shape}")

        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        lab = cv2.merge((l, a, b))
        img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        print("[Preprocess] Applied CLAHE")

        img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        print("[Preprocess] Denoised")

        kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
        img = cv2.filter2D(img, -1, kernel)
        print("[Preprocess] Applied sharpening filter")

        img = OCRService.pad_to_multiple(img, multiple=32)
        return img

    @staticmethod
    def pad_to_multiple(img: np.ndarray, multiple: int = 32) -> np.ndarray:
        h, w = img.shape[:2]
        new_h = ((h + multiple - 1) // multiple) * multiple
        new_w = ((w + multiple - 1) // multiple) * multiple
        pad_bottom = new_h - h
        pad_right = new_w - w
        padded = cv2.copyMakeBorder(img, 0, pad_bottom, 0, pad_right,
                                    borderType=cv2.BORDER_CONSTANT, value=[0,0,0])
        print(f"[Preprocess] Padded image {w}x{h} → {new_w}x{new_h}")
        return padded

    def extract_text(self, img_path: str) -> str:
        print(f"[OCRService] Processing {img_path}")
        if self.preprocess:
            img = self.load_and_preprocess(img_path)
        else:
            img = img_path

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

