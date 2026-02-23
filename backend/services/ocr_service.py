import cv2
import numpy as np
import paddle

paddle.set_device("cpu")
paddle.set_flags({'FLAGS_use_mkldnn': True})

from paddleocr import PaddleOCR
from .recognition_service import HandwritingRecognitionService
from .image_preprocessor import load_and_preprocess


class OCRService:
    def __init__(self):
        self.detector = PaddleOCR(
            use_angle_cls=True,
            lang='bg',
            det_limit_side_len=1536,
        )

        self.recognizer = HandwritingRecognitionService()

    def extract_text(self, image_path: str) -> str:
        print(f"[OCRService] Loading and preprocessing {image_path}")

        img = load_and_preprocess(image_path)

        result = self.detector.ocr(img)

        if not result:
            print("[OCRService] No detection result.")
            return ""

        if isinstance(result, dict):
            dt_polys = result.get("dt_polys", [])
            rec_scores = result.get("rec_scores", [])

        else:
            print("[OCRService] Unexpected result format.")
            return ""

        if not dt_polys:
            print("[OCRService] No text boxes detected.")
            return ""

        cropped_lines = []
        sorted_indices = sorted(
            range(len(dt_polys)),
            key=lambda i: (dt_polys[i][0][1], dt_polys[i][0][0])
        )

        for idx in sorted_indices:
            box = dt_polys[idx]

            if rec_scores and rec_scores[idx] < 0.4:
                continue

            crop = self._crop_polygon(img, box)

            if crop is None or crop.size == 0:
                continue

            try:
                text = self.recognizer.recognize(crop)
                if text.strip():
                    cropped_lines.append(text.strip())
            except Exception as e:
                print(f"[OCRService] Recognition error: {e}")

        full_text = "\n".join(cropped_lines)

        return full_text

    def _crop_polygon(self, image: np.ndarray, polygon: np.ndarray) -> np.ndarray:
        try:
            rect = cv2.boundingRect(polygon.astype(np.int32))
            x, y, w, h = rect

            cropped = image[y:y+h, x:x+w]

            return cropped
        except Exception as e:
            print(f"[OCRService] Crop error: {e}")
            return None
