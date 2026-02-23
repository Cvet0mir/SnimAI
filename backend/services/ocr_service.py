import paddle

paddle.set_device("cpu")
paddle.set_flags({'FLAGS_use_mkldnn': False})

from paddleocr import PaddleOCR
from .recognition_service import HandwritingRecognitionService

class OCRService:
    def __init__(self):
        self.detector = PaddleOCR(
            use_angle_cls=True,
            lang='bg',
        )
        self.recognizer = HandwritingRecognitionService()

    def extract_text(self, image_path: str) -> str:
        result = self.detector.predict(image_path)
        recognized_texts = []

        for line in result:
            detected_text = line[1][0]
            recognized_texts.append(detected_text)

        full_text = "\n".join(recognized_texts)
        return full_text
