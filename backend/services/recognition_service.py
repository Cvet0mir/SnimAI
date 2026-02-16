import torch
from PIL import Image
import cv2
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

from ..core.config import settings


class HandwritingRecognitionService:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.processor = TrOCRProcessor.from_pretrained(settings.HANDWRITING_MODEL_PATH)
        self.model = VisionEncoderDecoderModel.from_pretrained(settings.HANDWRITING_MODEL_PATH)

        self.model.to(self.device)
        self.model.eval()

    def recognize(self, cropped_images):
        if not cropped_images:
            return []

        pil_images = [
            Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            for img in cropped_images
        ]

        features = self.processor(
            images=pil_images,
            return_tensors="pt",
            padding=True
        )
        pixel_values = features["pixel_values"].to(self.device)

        with torch.no_grad():
            generated_ids = self.model.generate(
                pixel_values,
                num_beams=4,
                max_length=128
            )

        texts = self.processor.batch_decode(
            generated_ids,
            skip_special_tokens=True
        )

        return texts


