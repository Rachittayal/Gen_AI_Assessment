import pytest

from embedder.embedder import Embedder
from store.vector_store import VectorStore

SAMPLE_DOCS = [
    {"id": "doc_a", "text": "Load balancing distributes traffic across multiple servers."},
    {"id": "doc_b", "text": "Vector embeddings capture semantic meaning of text."},
    {"id": "doc_c", "text": "Database replication keeps copies of data on different nodes."},
    {"id": "doc_d", "text": "Caching stores frequently accessed data in fast memory."},
    {"id": "doc_e", "text": "Cosine similarity measures the angle between two vectors."},
]

@pytest.fixture(scope="module")
def store():
    embedder = Embedder()
    vs = VectorStore(embedder)
    vs.ingest(SAMPLE_DOCS)
    return vs

def test_search_returns_list(store):
    query_vector = store.embedder.embed("test query")
    results = store.search(query_vector, top_k=3)
    assert isinstance(results, list)

def test_search_returns_correct_count(store):
    query_vector = store.embedder.embed("servers and traffic")
    results = store.search(query_vector, top_k=3)
    assert len(results) == 3

def test_search_result_has_required_keys(store):
    query_vector = store.embedder.embed("embeddings and vectors")
    results = store.search(query_vector, top_k=1)
    assert "id" in results[0]
    assert "score" in results[0]
    assert "text" in results[0]

def test_search_scores_are_descending(store):
    query_vector = store.embedder.embed("database and replication")
    results = store.search(query_vector, top_k=3)
    scores = [r["score"] for r in results]
    assert scores == sorted(scores, reverse=True)

def test_search_most_relevant_doc_ranked_first(store):
    query_vector = store.embedder.embed("cosine angle between vectors similarity")
    results = store.search(query_vector, top_k=5)
    assert results[0]["id"] == "doc_e"

def test_search_before_ingest_raises_error():
    empty_store = VectorStore(Embedder())
    query_vector = empty_store.embedder.embed("anything")
    with pytest.raises(RuntimeError, match="Call ingest\\(\\) before search"):
        empty_store.search(query_vector)