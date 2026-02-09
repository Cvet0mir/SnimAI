from ..ml.embedding_model import embedding_model
from ..core.config import settings

import faiss
import numpy as np

dimension = 384
index = faiss.IndexFlatL2(dimension)
documents = []

def add_chunks_to_index(chunks: int = settings.CHUNK_SIZE):
    global documents
    vectors = embedding_model.encode(chunks)
    index.add(np.array(vectors, dtype='float32'))
    documents.extend(chunks)

def retrieve_relevant(query, top_k: int = settings.TOP_K):
    query_vector = embedding_model.encode([query])
    D, I = index.search(np.array(query_vector, dtype='float32'), top_k)
    return [documents[i] for i in I[0]]

