from sentence_transformers import SentenceTransformer
import numpy as np


class Embedder:
    MODEL_NAME = "all-MiniLM-L6-v2"

    def __init__(self):
        self.model=SentenceTransformer(self.MODEL_NAME)

    def embed(self, text):
        vector=self.model.encode([text],convert_to_numpy=True)[0]
        return vector.astype(np.float32)

    def embed_many(self, texts):
        vectors=self.model.encode(texts, convert_to_numpy=True)
        return vectors.astype(np.float32)