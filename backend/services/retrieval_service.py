import faiss
import numpy as np
from ..ml.embedding_model import embedding_model

from ..core.config import settings

DIM = 384

class RetrievalService:
    def __init__(self):
        self._indices = {}
        self._chunks = {}

    def index_text(self, session_id: int, text: str, chunk_size: int = settings.CHUNK_SIZE):
        words = text.split()
        chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

        vectors = embedding_model.encode(chunks)

        if session_id not in self._indices:
            index = faiss.IndexFlatL2(DIM)
            self._indices[session_id] = index
            self._chunks[session_id] = []
        else:
            index = self._indices[session_id]

        index.add(np.array(vectors, dtype="float32"))
        self._chunks[session_id].extend(chunks)

    def retrieve_chunks(self, session_id: int, query: str, top_k: int = settings.TOP_K) -> list[str]:
        if session_id not in self._indices or not self._chunks[session_id]:
            return []

        q_vec = embedding_model.encode([query])
        _, I = self._indices[session_id].search(np.array(q_vec, dtype="float32"), top_k)
        return [self._chunks[session_id][i] for i in I[0]]

    def reset_session(self, session_id: int):
        if session_id in self._indices:
            del self._indices[session_id]
            del self._chunks[session_id]
            
