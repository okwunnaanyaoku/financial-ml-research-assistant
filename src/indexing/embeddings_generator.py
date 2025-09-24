from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

class EmbeddingsGenerator:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, normalize_embeddings=True)

    def generate_single_embedding(self, text: str) -> np.ndarray:
        return self.model.encode([text], normalize_embeddings=True)[0]