# Retrieval Benchmark: Strategy A vs Strategy B

Generated: 2026-05-16T22:59:46
Top-K: 3

---

## Query: How does the system handle peak load?

### Strategy A - Raw Vector Search

| Rank | Doc ID | Score | Preview |
|------|--------|-------|---------|
| 1 | doc_01 | 0.734 | Peak load handling is managed through a combination of horizontal scaling and au... |
| 2 | doc_04 | 0.3561 | Caching is a technique for storing frequently accessed data in fast memory so it... |
| 3 | doc_08 | 0.3164 | Message queues decouple producers and consumers in a distributed system. The pro... |

### Strategy B - AI Enhanced Retrieval

Expanded query: autoscaling load balancing high traffic horizontal scaling traffic spike

| Rank | Doc ID | Score | Preview |
|------|--------|-------|---------|
| 1 | doc_01 | 0.644 | Peak load handling is managed through a combination of horizontal scaling and au... |
| 2 | doc_08 | 0.3242 | Message queues decouple producers and consumers in a distributed system. The pro... |
| 3 | doc_06 | 0.2697 | Rate limiting protects backend services from being overwhelmed by too many reque... |

Both strategies returned: doc_01, doc_08

---

## Query: What similarity metric is used for vector search?

### Strategy A - Raw Vector Search

| Rank | Doc ID | Score | Preview |
|------|--------|-------|---------|
| 1 | doc_05 | 0.6154 | The FAISS library (Facebook AI Similarity Search) provides efficient algorithms ... |
| 2 | doc_02 | 0.5865 | Vector embeddings are numerical representations of text that capture semantic me... |
| 3 | doc_07 | 0.4893 | Cosine similarity measures the angle between two vectors rather than the distanc... |

### Strategy B - AI Enhanced Retrieval

Expanded query: cosine similarity euclidean distance dot product nearest neighbour

| Rank | Doc ID | Score | Preview |
|------|--------|-------|---------|
| 1 | doc_07 | 0.6172 | Cosine similarity measures the angle between two vectors rather than the distanc... |
| 2 | doc_05 | 0.4425 | The FAISS library (Facebook AI Similarity Search) provides efficient algorithms ... |
| 3 | doc_02 | 0.297 | Vector embeddings are numerical representations of text that capture semantic me... |

Both strategies returned: doc_02, doc_05, doc_07

---

## Query: How is data kept available if a node fails?

### Strategy A - Raw Vector Search

| Rank | Doc ID | Score | Preview |
|------|--------|-------|---------|
| 1 | doc_03 | 0.5259 | Database replication ensures high availability by maintaining multiple copies of... |
| 2 | doc_08 | 0.3064 | Message queues decouple producers and consumers in a distributed system. The pro... |
| 3 | doc_04 | 0.2704 | Caching is a technique for storing frequently accessed data in fast memory so it... |

### Strategy B - AI Enhanced Retrieval

Expanded query: failover replication high availability backup recovery redundancy

| Rank | Doc ID | Score | Preview |
|------|--------|-------|---------|
| 1 | doc_03 | 0.6531 | Database replication ensures high availability by maintaining multiple copies of... |
| 2 | doc_01 | 0.2333 | Peak load handling is managed through a combination of horizontal scaling and au... |
| 3 | doc_08 | 0.205 | Message queues decouple producers and consumers in a distributed system. The pro... |

Both strategies returned: doc_03, doc_08

---

## Notes

### Why cosine similarity and not Euclidean distance

For text embeddings only the direction of a vector carries meaning.
The magnitude is an artefact of sentence length and has no semantic value.
Cosine similarity measures the angle between two vectors and ignores magnitude.
Euclidean distance is affected by magnitude which makes it unreliable for text.
In FAISS we normalise all vectors to unit length and use IndexFlatIP.
Inner product on normalised vectors equals cosine similarity.

### How to migrate to Vertex AI Vector Search in production

1. Export embeddings to a JSONL file with id and vector per line.
2. Upload the JSONL file to a Cloud Storage bucket.
3. Create a MatchingEngineIndex resource via the Vertex AI API.
4. Deploy the index to an IndexEndpoint to get a live endpoint.
5. Replace VectorStore.search() with Vertex AI find_neighbors() calls.
The embedding model stays the same. Only the search layer changes.
