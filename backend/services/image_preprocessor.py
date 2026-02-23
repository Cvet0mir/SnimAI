import cv2
import numpy as np

MAX_DIM = 1600
USE_GRAYSCALE = True

def load_and_preprocess(image_path: str) -> np.ndarray:
    img = cv2.imread(image_path)
    
    if img is None:
        raise FileNotFoundError(f"Could not load image at path: {image_path}")

    height, width = img.shape[:2]
    if max(width, height) > MAX_DIM:
        scale = MAX_DIM / max(width, height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        img = cv2.resize(img, (new_width, new_height))
        print(f"[Preprocess] Resized image from {width}x{height} → {new_width}x{new_height}")

    if USE_GRAYSCALE:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    return img