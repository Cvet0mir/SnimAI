from paddleocr import PaddleOCR
from .recognition_service import HandwritingRecognitionService

class OCRService:
    def __init__(self):
        self.detector = PaddleOCR(lang='bg')
        self.recognizer = HandwritingRecognitionService()

    def extract_text(self, image_path: str) -> str:
        result = self.detector.predict(image_path, cls=False)
        recognized_texts = []

        for line in result:
            detected_text = line[1][0]
            recognized_texts.append(detected_text)

        full_text = "\n".join(recognized_texts)
        return full_text
