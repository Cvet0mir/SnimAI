from sentence_transformers import SentenceTransformer
from ..core.config import settings

embedding_model = SentenceTransformer(settings.EMBEDDINGS_MODEL_PATH)
