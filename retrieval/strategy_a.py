class StrategyA:
    def __init__(self, embedder,vector_store):
        self.embedder=embedder
        self.vector_store=vector_store

    def retrieve(self,query,top_k=3):
        query_vector=self.embedder.embed(query)

        results=self.vector_store.search(query_vector, top_k=top_k)

        return results