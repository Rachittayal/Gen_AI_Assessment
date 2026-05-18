DOCUMENTS=[
    {
        "id": "doc_01",
        "text":(
            "Peak load handling is managed through a combination of horizontal scaling "
            "and autoscaling policies. When incoming traffic exceeds a defined threshold, "
            "the orchestration layer automatically provisions additional compute instances. "
            "Load balancers distribute requests evenly across all active nodes, and a "
            "circuit breaker pattern prevents any single service from becoming overwhelmed."
        ),
    },
    {
        "id": "doc_02",
        "text":(
            "Vector embeddings are numerical representations of text that capture semantic "
            "meaning. Two sentences with the same meaning but different words will produce "
            "embedding vectors that are close together in high-dimensional space. This property "
            "makes embeddings ideal for similarity search, where the goal is to find documents "
            "that are conceptually related to a query rather than just matching keywords."
        ),
    },
    {
        "id": "doc_03",
        "text":(
            "Database replication ensures high availability by maintaining multiple copies of "
            "the data across different nodes. In a primary-replica setup, all writes go to the "
            "primary node and are then propagated to replicas asynchronously. During a failover "
            "event, one of the replicas is promoted to primary, minimising downtime and ensuring "
            "the system continues to serve read and write requests."
        ),
    },
    {
        "id": "doc_04",
        "text":(
            "Caching is a technique for storing frequently accessed data in fast memory so it "
            "does not need to be recomputed or fetched from a slow backend on every request. "
            "Common caching strategies include LRU (Least Recently Used) eviction, TTL-based "
            "expiry, and write-through caching. A well-tuned cache can reduce database load "
            "by over 80 percent and bring response times down from hundreds of milliseconds "
            "to single-digit milliseconds."
        ),
    },
    {
        "id": "doc_05",
        "text":(
            "The FAISS library (Facebook AI Similarity Search) provides efficient algorithms "
            "for searching large collections of dense vectors. It supports both exact and "
            "approximate nearest-neighbour search. The IndexFlatIP index performs exact inner "
            "product search, while IndexIVFFlat partitions the space into clusters for faster "
            "approximate search. For most RAG applications with under one million vectors, "
            "IndexFlatL2 or IndexFlatIP gives acceptable speed with perfect recall."
        ),
    },
    {
        "id": "doc_06",
        "text":(
            "Rate limiting protects backend services from being overwhelmed by too many requests "
            "in a short period of time. The token bucket algorithm allows short bursts of traffic "
            "while enforcing an average rate limit over time. When a client exceeds the limit, "
            "the API gateway returns a 429 status code. Rate limits are typically applied per "
            "API key or per IP address and are configured separately for each endpoint."
        ),
    },
    {
        "id": "doc_07",
        "text":(
            "Cosine similarity measures the angle between two vectors rather than the distance "
            "between them. It is the preferred similarity metric for text embeddings because "
            "the magnitude of an embedding vector is not meaningful — only the direction matters. "
            "A cosine similarity of 1.0 means the two vectors point in exactly the same direction "
            "(identical meaning), while 0.0 means they are orthogonal (unrelated), and -1.0 means "
            "they are opposite in meaning."
        ),
    },
    {
        "id": "doc_08",
        "text":(
            "Message queues decouple producers and consumers in a distributed system. The producer "
            "places a message on the queue and continues without waiting for a response. The consumer "
            "reads from the queue at its own pace. This pattern smooths out traffic spikes: even if "
            "ten thousand events arrive in one second, the consumer processes them steadily without "
            "dropping any. RabbitMQ, Kafka, and Google Pub/Sub are common message queue systems."
        ),
    },
    {
        "id": "doc_09",
        "text":(
            "Query expansion is a technique used in information retrieval to improve recall. The "
            "original user query is rewritten or enriched with synonyms, related terms, and "
            "contextual information before being used to search the index. In an AI-enhanced "
            "pipeline, a language model performs this expansion step automatically. For example, "
            "the query 'peak load' might be expanded to 'high traffic, autoscaling, load balancing, "
            "burst capacity, horizontal scaling under peak demand'."
        ),
    },
    {
        "id": "doc_10",
        "text":(
            "Vertex AI Vector Search (formerly Matching Engine) is Google Cloud's managed service "
            "for high-scale approximate nearest-neighbour search. It uses the ScaNN algorithm "
            "internally and can handle billions of vectors with low latency. To migrate a local "
            "FAISS index to Vertex AI, you export your embeddings as a JSONL file, upload them "
            "to a Cloud Storage bucket, and create an Index resource via the Vertex AI API. "
            "The deployed index then serves queries through a gRPC or HTTP endpoint."
        ),
    },
]