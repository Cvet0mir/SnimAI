from .detection_service import TextDetectionService
from .recognition_service import HandwritingRecognitionService


class OCRService:
    def __init__(self):
        self.detector = TextDetectionService()
        self.recognizer = HandwritingRecognitionService()

    def extract_text(self, image_path: str) -> str:
        boxes = self.detector.detect_boxes(image_path)
        if not boxes:
            return ""

        cropped_images = self.detector.crop_boxes(image_path, boxes)
        texts = self.recognizer.recognize(cropped_images)

        return "\n".join(texts)
