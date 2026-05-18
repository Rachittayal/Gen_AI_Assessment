from data.corpus import DOCUMENTS
from embedder.embedder import Embedder
from store.vector_store import VectorStore
from retrieval.strategy_a import StrategyA
from retrieval.strategy_b import StrategyB
from mocks.vertex_mocks import MockGenerativeModel
from benchmark.benchmarker import Benchmarker


def build_pipeline():
    embedder=Embedder()
    print(f"Model loaded {Embedder.MODEL_NAME}")

    print("\nIngest")
    vector_store=VectorStore(embedder)
    vector_store.ingest(DOCUMENTS)

    strategy_a=StrategyA(embedder, vector_store)

    generative_model=MockGenerativeModel("Lukavest")
    strategy_b=StrategyB(embedder,vector_store,generative_model)

    print("Strategy A ready.")
    print("Strategy B ready.")

    benchmarker = Benchmarker(strategy_a, strategy_b)

    return benchmarker

def main():
    benchmarker=build_pipeline()

    print("\nRunning benchmark...")
    report=benchmarker.run(top_k=3)

    benchmarker.save_json(report)
    benchmarker.save_markdown(report)

    print("Files: retrieval_benchmark.json, retrieval_benchmark.md")

if __name__ == "__main__":
    main()