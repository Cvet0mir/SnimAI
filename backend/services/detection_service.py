import cv2
from paddleocr import PaddleOCR


class TextDetectionService:
    def __init__(self):
        self.detector = PaddleOCR(
            use_angle_cls=True,
            lang="en",
            rec=False
        )

    def detect_boxes(self, image_path: str):
        results = self.detector.predict(image_path, cls=True)

        if not results or not results[0]:
            return []

        boxes = [line[0] for line in results[0]]
        return self._sort_boxes(boxes)

    @staticmethod
    def _sort_boxes(boxes):
        return sorted(boxes, key=lambda b: (b[0][1], b[0][0]))

    @staticmethod
    def crop_boxes(image_path: str, boxes):
        image = cv2.imread(image_path)
        cropped_images = []

        for box in boxes:
            box = list(map(lambda p: [int(p[0]), int(p[1])], box))

            x_min = min(p[0] for p in box)
            x_max = max(p[0] for p in box)
            y_min = min(p[1] for p in box)
            y_max = max(p[1] for p in box)

            cropped = image[y_min:y_max, x_min:x_max]

            if cropped.size != 0:
                cropped_images.append(cropped)

        return cropped_images


