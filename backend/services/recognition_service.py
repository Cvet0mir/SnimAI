from transformers import VisionEncoderDecoderModel, AutoProcessor
from PIL import Image
import torch
import numpy as np

from ..core.config import settings


class HandwritingRecognitionService:
    def __init__(self):
        model_name = settings.HANDWRITING_MODEL_PATH

        self.model = VisionEncoderDecoderModel.from_pretrained(model_name)
        self.processor = AutoProcessor.from_pretrained(model_name)

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def recognize(self, image: np.ndarray) -> str:
        if len(image.shape) == 3:
            image = image[:, :, ::-1]

        pil_image = Image.fromarray(image).convert("RGB")

        pixel_values = self.processor(
            images=pil_image,
            return_tensors="pt"
        ).pixel_values.to(self.device)

        generated_ids = self.model.generate(pixel_values)

        text = self.processor.batch_decode(
            generated_ids,
            skip_special_tokens=True
        )[0]

        return text.strip()
