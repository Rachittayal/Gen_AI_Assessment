from embedder.embedder import Embedder
from store.vector_store import VectorStore

class StrategyB:
    def __init__(self,embedder,vector_store,generative_model):
        self.embedder=embedder
        self.vector_store=vector_store
        self.generative_model=generative_model

    def build_prompt(self,query):
        prompt=(
            "You are a search assistant.\n"
            "Rewrite the query below using more technical terms and synonyms.\n"
            "Return only the expanded query. No explanation.\n\n"
            "Query: " + query + "\n\n"
            "Expanded query:"
        )
        return prompt

    def expand_query(self,query):
        prompt=self.build_prompt(query)
        response=self.generative_model.generate_content(prompt)
        expanded=response.text.strip()
        return expanded

    def retrieve(self,query,top_k=3):
        expanded_query=self.expand_query(query)

        query_vector=self.embedder.embed(expanded_query)

        results=self.vector_store.search(query_vector, top_k=top_k)

        output={"expanded_query": expanded_query,"results": results,}

        return output