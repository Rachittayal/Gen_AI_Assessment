import json
from datetime import datetime


BENCHMARK_QUERIES = [
    "How does the system handle peak load?",
    "What similarity metric is used for vector search?",
    "How is data kept available if a node fails?",
]


class Benchmarker:
    def __init__(self, strategy_a, strategy_b):
        self.strategy_a=strategy_a
        self.strategy_b=strategy_b

    def run(self, queries=None, top_k=3):
        if queries is None:
            queries=BENCHMARK_QUERIES

        report={
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "top_k": top_k,
            "results": [],
        }

        for query in queries:
            print(f"\nRunning query:'{query}'")

            a_results=self.strategy_a.retrieve(query,top_k=top_k)
            print(f"Strategy A top result: {a_results[0]['id']} "
                  f"(score={a_results[0]['score']})")

            b_output=self.strategy_b.retrieve(query, top_k=top_k)
            b_results = b_output["results"]
            expanded_query = b_output["expanded_query"]
            print(f"  Expanded query: '{expanded_query[:80]}...'")
            print(f"  Strategy B top result: {b_results[0]['id']} "
                  f"(score={b_results[0]['score']})")

            a_ids = {r["id"] for r in a_results}
            b_ids = {r["id"] for r in b_results}
            overlap = sorted(a_ids & b_ids)

            report["results"].append({
                "query": query,
                "strategy_a": {"results": a_results},
                "strategy_b": {"expanded_query": expanded_query, "results": b_results},
                "overlap": overlap,
            })

        return report

    def save_json(self, report, filepath="retrieval_benchmark.json"):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"\nJSON report saved to: {filepath}")

    def save_markdown(self, report, filepath="retrieval_benchmark.md"):
        content = ""
        content += "# Retrieval Benchmark: Strategy A vs Strategy B\n\n"
        content += f"Generated: {report['generated_at']}\n"
        content += f"Top-K: {report['top_k']}\n\n"
        content += "---\n\n"

        for entry in report["results"]:
            content += f"## Query: {entry['query']}\n\n"

            content += "### Strategy A - Raw Vector Search\n\n"
            content += "| Rank | Doc ID | Score | Preview |\n"
            content += "|------|--------|-------|---------|\n"
            for rank, result in enumerate(entry["strategy_a"]["results"], start=1):
                preview = result["text"][:80] + "..."
                content += f"| {rank} | {result['id']} | {result['score']} | {preview} |\n"

            content += "\n"

            content += "### Strategy B - AI Enhanced Retrieval\n\n"
            content += f"Expanded query: {entry['strategy_b']['expanded_query']}\n\n"
            content += "| Rank | Doc ID | Score | Preview |\n"
            content += "|------|--------|-------|---------|\n"
            for rank, result in enumerate(entry["strategy_b"]["results"], start=1):
                preview = result["text"][:80] + "..."
                content += f"| {rank} | {result['id']} | {result['score']} | {preview} |\n"

            content += "\n"

            if entry["overlap"]:
                content += f"Both strategies returned: {', '.join(entry['overlap'])}\n\n"
            else:
                content += "No overlap — both strategies returned different results.\n\n"

            content += "---\n\n"

        content += "## Notes\n\n"

        content += "### Why cosine similarity and not Euclidean distance\n\n"
        content += (
            "For text embeddings only the direction of a vector carries meaning.\n"
            "The magnitude is an artefact of sentence length and has no semantic value.\n"
            "Cosine similarity measures the angle between two vectors and ignores magnitude.\n"
            "Euclidean distance is affected by magnitude which makes it unreliable for text.\n"
            "In FAISS we normalise all vectors to unit length and use IndexFlatIP.\n"
            "Inner product on normalised vectors equals cosine similarity.\n\n"
        )

        content += "### How to migrate to Vertex AI Vector Search in production\n\n"
        content += (
            "1. Export embeddings to a JSONL file with id and vector per line.\n"
            "2. Upload the JSONL file to a Cloud Storage bucket.\n"
            "3. Create a MatchingEngineIndex resource via the Vertex AI API.\n"
            "4. Deploy the index to an IndexEndpoint to get a live endpoint.\n"
            "5. Replace VectorStore.search() with Vertex AI find_neighbors() calls.\n"
            "The embedding model stays the same. Only the search layer changes.\n"
        )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Markdown report saved to: {filepath}")
        
if __name__ == "__main__":
    import sys
    import os

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    from embedder.embedder import Embedder
    from store.vector_store import VectorStore
    from retrieval.strategy_a import StrategyA
    from retrieval.strategy_b import StrategyB
    from mocks.vertex_mocks import MockGenerativeModel
    from data.corpus import DOCUMENTS

    print("Setting up pipeline...")

    embedder = Embedder()
    vector_store = VectorStore(embedder)
    vector_store.ingest(DOCUMENTS)

    strategy_a = StrategyA(embedder, vector_store)
    strategy_b = StrategyB(embedder, vector_store, MockGenerativeModel("gemini-pro"))

    benchmarker = Benchmarker(strategy_a, strategy_b)

    report = benchmarker.run()

    benchmarker.save_json(report)
    benchmarker.save_markdown(report)

    print("\nDone. Check retrieval_benchmark.json and retrieval_benchmark.md")