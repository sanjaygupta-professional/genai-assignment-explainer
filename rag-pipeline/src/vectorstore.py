"""Qdrant vector store wrapper — file-persisted, no Docker needed.

Uses COSINE distance with 768-dimensional vectors from Gemini Embedding 2.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchAny,
)
from src.config import QDRANT_DIR, QDRANT_COLLECTION, EMBEDDING_DIMS

_client = None


def get_client() -> QdrantClient:
    """Get file-persisted Qdrant client."""
    global _client
    if _client is None:
        QDRANT_DIR.mkdir(parents=True, exist_ok=True)
        _client = QdrantClient(path=str(QDRANT_DIR))
    return _client


def create_collection() -> None:
    """Create the vector collection if it doesn't exist."""
    client = get_client()
    collections = [c.name for c in client.get_collections().collections]
    if QDRANT_COLLECTION not in collections:
        client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=EMBEDDING_DIMS,
                distance=Distance.COSINE,
            ),
        )


def upsert_chunks(
    chunk_ids: list[str],
    vectors: list[list[float]],
    payloads: list[dict],
) -> None:
    """Upsert embedded chunks into Qdrant."""
    client = get_client()
    points = []
    for i, (cid, vec, payload) in enumerate(zip(chunk_ids, vectors, payloads)):
        points.append(PointStruct(
            id=i,  # Qdrant needs int or UUID
            vector=vec,
            payload={"chunk_id": cid, **payload},
        ))
    # Batch upsert
    BATCH_SIZE = 64
    for start in range(0, len(points), BATCH_SIZE):
        batch = points[start : start + BATCH_SIZE]
        client.upsert(collection_name=QDRANT_COLLECTION, points=batch)


def search(
    query_vector: list[float],
    top_k: int = 5,
    scheme_ids: list[str] | None = None,
) -> list[dict]:
    """Search for similar chunks, optionally filtered to specific scheme IDs.

    Args:
        query_vector: 768-dim query embedding
        top_k: number of results
        scheme_ids: if provided, only search within these scheme IDs (from KG)
    """
    client = get_client()

    query_filter = None
    if scheme_ids:
        query_filter = Filter(must=[
            FieldCondition(
                key="scheme_id",
                match=MatchAny(any=scheme_ids),
            )
        ])

    results = client.query_points(
        collection_name=QDRANT_COLLECTION,
        query=query_vector,
        limit=top_k,
        query_filter=query_filter,
    )
    return [
        {
            "chunk_id": hit.payload.get("chunk_id", ""),
            "scheme_id": hit.payload.get("scheme_id", ""),
            "source_pdf": hit.payload.get("source_pdf", ""),
            "page_range": hit.payload.get("page_range", ""),
            "text": hit.payload.get("text", ""),
            "score": hit.score,
        }
        for hit in results.points
    ]


def get_collection_info() -> dict:
    """Get collection stats."""
    client = get_client()
    try:
        info = client.get_collection(QDRANT_COLLECTION)
        return {
            "name": QDRANT_COLLECTION,
            "points_count": info.points_count,
            "vectors_count": info.vectors_count,
        }
    except Exception:
        return {"name": QDRANT_COLLECTION, "points_count": 0}
