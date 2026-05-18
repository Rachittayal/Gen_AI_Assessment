import numpy as np

class FakeEmbeddingResult:
    def __init__(self, vector):
        self.values = vector


class FakeResponse:
    pass

class MockTextEmbeddingModel:

    EMBEDDING_DIM = 384

    @classmethod
    def from_pretrained(cls, model_name):
        obj=cls()
        obj.model_name=model_name 
        return obj

    def get_embeddings(self, texts):
        results = []

        for text in texts:
            text_hash = abs(hash(text))
            print(f"Hash for '{text}': {text_hash}")
            
            seed = text_hash % (2 ** 32)
            print(seed)
            rng = np.random.default_rng(seed)
            print(rng)
            vector = rng.random(self.EMBEDDING_DIM)
            print(vector)
            

            vector = vector.astype(np.float32)
            print(vector)

            vector = vector.tolist()
            print(vector)

            result = FakeEmbeddingResult(vector)
            print(result)
            results.append(result)

        return results


class MockGenerativeModel:

    def __init__(self, model_name):
        self.model_name = model_name

        self.query_expansions = {
            "How does the system handle peak load?":
                "autoscaling load balancing high traffic horizontal scaling traffic spike",

            "What similarity metric is used for vector search?":
                "cosine similarity euclidean distance dot product nearest neighbour",

            "How is data kept available if a node fails?":
                "failover replication high availability backup recovery redundancy",
        }

    def generate_content(self, prompt):
        query=self._get_query(prompt)

        if query in self.query_expansions:
            expanded=self.query_expansions[query]
        else:
            expanded=query+" related concepts details"

        response=FakeResponse()
        response.text=expanded
        return response

    def _get_query(self, prompt):
        lines=prompt.split("\n")
        for line in lines:
            line=line.strip()
            if line.startswith("Query:"):
                actual_query = line.replace("Query:", "").strip()
                return actual_query

        return prompt.strip()
    