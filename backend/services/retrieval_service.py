import faiss
import numpy as np
from ..ml.embedding_model import embedding_model

DIM = 384
_index = faiss.IndexFlatL2(DIM)
_chunks: list[str] = []


def index_text(text: str, chunk_size: int = 400):
    words = text.split()
    chunks = [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]

    vectors = embedding_model.encode(chunks)
    _index.add(np.array(vectors, dtype="float32"))
    _chunks.extend(chunks)


def retrieve_chunks(query: str, top_k: int = 5) -> list[str]:
    q_vec = embedding_model.encode([query])
    _, I = _index.search(np.array(q_vec, dtype="float32"), top_k)
    return [_chunks[i] for i in I[0]]
