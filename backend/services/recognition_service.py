from transformers import VisionEncoderDecoderModel, AutoProcessor
from PIL import Image
import torch
import os

from ..core.config import settings

class HandwritingRecognitionService:
    def __init__(self):
        model_name = settings.HANDWRITING_MODEL_PATH
        self.model = VisionEncoderDecoderModel.from_pretrained(model_name)
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def recognize(self, image_path: str) -> str:
        image = Image.open(image_path).convert("RGB")
        pixel_values = self.processor(images=image, return_tensors="pt").pixel_values.to(self.device)
        generated_ids = self.model.generate(pixel_values)
        text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return text
