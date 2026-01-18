from PIL import Image

def load_image(path):
    return Image.open(path).convert("RGB")

def resize_image(image, max_size: int = 1600):
    w, h = image.size
    scale = min(max_size / max(w, h), 1.0)
    return image.resize((int(w*scale), int(h*scale)))
