# Similarity Metric Choice & Vertex AI Vector Search Migration

## Table of Contents

- [Similarity Metric Choice](#similarity-metric-choice)
  - [Why Cosine Similarity?](#why-cosine-similarity)
  - [Cosine Similarity vs. Euclidean Distance](#cosine-similarity-vs-euclidean-distance)
  - [Implementation Detail](#implementation-detail)
- [Production Migration to Vertex AI Vector Search](#production-migration-to-vertex-ai-vector-search)
  - [Migration Architecture](#migration-architecture)
  - [Step-by-Step Migration Guide](#step-by-step-migration-guide)
  - [Why This Migration Is Practical](#why-this-migration-is-practical)

---

## Similarity Metric Choice

### Why Cosine Similarity?

This project generates semantic text embeddings using:

python
SentenceTransformer("all-MiniLM-L6-v2")


Embedding models encode text as high-dimensional vectors where **semantic meaning is captured by the direction of the vector**, not its magnitude. Because of this property, **cosine similarity is a better fit than Euclidean distance** for text retrieval tasks.

---

### Cosine Similarity vs. Euclidean Distance

| Property | Cosine Similarity | Euclidean Distance |
|---|---|---|
| Measures | Angle between vectors | Straight-line distance between vectors |
| Sensitive to magnitude? | No | Yes |
| Best for | NLP / semantic search | Geometric / spatial problems |
| Reliability for embeddings | High | Lower (affected by sentence length, model behaviour) |

#### Cosine Similarity

**Formula:**

$$\cos(A, B) = \frac{A \cdot B}{\|A\| \times \|B\|}$$

Cosine similarity focuses purely on the **direction** of two vectors, ignoring their magnitude. This is ideal for semantic search because two sentences can have the same meaning but produce vectors of different magnitudes.

**Example:**


"high traffic handling"
"peak load management"


Even though the wording differs, both phrases point in a similar direction in the embedding space — and cosine similarity correctly identifies them as semantically related, regardless of vector magnitude.

#### Euclidean Distance

**Formula:**

$$\text{distance}(A, B) = \sqrt{\sum (A_i - B_i)^2}$$

Euclidean distance is sensitive to vector magnitude. In embedding systems, magnitude can vary due to sentence length or model internals — even when two sentences are semantically identical. This makes Euclidean distance less reliable for semantic text retrieval.

---

### Implementation Detail

This project uses FAISS with inner product search on L2-normalised vectors:

python
import faiss

# Normalise vectors to unit length
faiss.normalize_L2(vectors)

# Create an inner product index
index = faiss.IndexFlatIP(dimension)


After L2 normalisation, every vector satisfies:


||vector|| = 1


This makes **inner product search mathematically equivalent to cosine similarity search** — a standard pattern used in production retrieval systems.

**Why IndexFlatIP?**

IndexFlatIP performs **exact nearest-neighbour search** using inner product similarity.

- Perfect recall — no approximation error
- Simple setup with no tuning required
- Accurate retrieval results
- Appropriate for assessment-scale or small-to-medium datasets

---

## Production Migration to Vertex AI Vector Search

The current implementation uses a **local FAISS index**. For production deployment at scale, the retrieval layer can be migrated to **Google Cloud Vertex AI Vector Search** (formerly Matching Engine), which supports:

- Billion-scale vector datasets
- Distributed and managed indexing
- Low-latency retrieval
- Approximate nearest-neighbour (ANN) search via Google's **ScaNN** algorithm

---

### Migration Architecture


Documents
    ↓
Embedding Model  (unchanged)
    ↓
Generated Embeddings
    ↓
JSONL Export
    ↓
Google Cloud Storage (GCS)
    ↓
Vertex AI Vector Search Index
    ↓
Index Endpoint Deployment
    ↓
Semantic Retrieval API


---

### Step-by-Step Migration Guide

#### Step 1 — Generate Embeddings

Use the existing embedding pipeline. **No changes to the embedding model are required.**

python
vector = embedder.embed(text)


#### Step 2 — Export Embeddings to JSONL

Export all embeddings into JSONL format. Each line must contain a document ID and its embedding vector.

json
{"id": "doc_01", "embedding": [0.12, 0.45, 0.91]}
{"id": "doc_02", "embedding": [0.33, 0.71, 0.55]}


#### Step 3 — Upload to Google Cloud Storage

Upload the JSONL file to a GCS bucket:

bash
gsutil cp embeddings.jsonl gs://my-bucket/embeddings/data.jsonl


#### Step 4 — Create a Vertex AI Vector Search Index

Create a MatchingEngineIndex resource using the Vertex AI SDK. Vertex AI will build an optimised ANN structure (ScaNN) internally.

python
from google.cloud import aiplatform

aiplatform.init(project="my-project", location="us-central1")

index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
    display_name="my-vector-index",
    contents_delta_uri="gs://my-bucket/embeddings/",
    dimensions=384,           # Match your embedding model output size
    approximate_neighbors_count=10,
)


#### Step 5 — Deploy an Index Endpoint

Deploy the index to an IndexEndpoint to create a scalable serving layer:

python
index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
    display_name="my-index-endpoint",
    public_endpoint_enabled=True,
)

index_endpoint.deploy_index(
    index=index,
    deployed_index_id="my_deployed_index",
)


#### Step 6 — Replace Local FAISS Calls

**Before (local FAISS):**

python
results = vector_store.search(query_vector)


**After (Vertex AI Vector Search):**

python
results = index_endpoint.find_neighbors(
    deployed_index_id="my_deployed_index",
    queries=[query_vector],
    num_neighbors=10,
)


The retrieval logic remains largely the same. **Only the vector database backend changes.**

---

### Why This Migration Is Practical

The project is built with a **modular, layered architecture**:


┌─────────────────────┐
│   Embedding Layer   │  — Generates vectors from text
├─────────────────────┤
│   Retrieval Layer   │  — Handles query logic
├─────────────────────┤
│  Vector Store Layer │  — vector_store.py (FAISS → Vertex AI)
└─────────────────────┘


Because vector search logic is **isolated inside `vector_store.py`**, replacing FAISS with Vertex AI requires minimal changes to the rest of the codebase. The embedding layer and retrieval logic remain entirely untouched.

This clean separation makes the pipeline **production-ready and straightforward to scale**.
