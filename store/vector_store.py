import faiss
import numpy as np

class VectorStore:
    def __init__(self, embedder):
        self.embedder=embedder

        self.index=None

        self.documents=[]

    def ingest(self, documents):
        texts=[doc["text"] for doc in documents]

        vectors=self.embedder.embed_many(texts)

        faiss.normalize_L2(vectors)

        embedding_dim=vectors.shape[1]
        self.index=faiss.IndexFlatIP(embedding_dim)

        self.index.add(vectors)

        self.documents = documents


    def search(self, query_vector, top_k=3):
        if self.index is None:
            raise RuntimeError("VectorStore is empty. Call ingest() before search.")

        query=query_vector.reshape(1,-1).astype(np.float32)

        faiss.normalize_L2(query)

        scores, indices = self.index.search(query, top_k)

        results=[]
        for score, idx in zip(scores[0], indices[0]):
            doc = self.documents[idx]
            results.append({"id": doc["id"],"score": round(float(score), 4),"text": doc["text"],})

        return results