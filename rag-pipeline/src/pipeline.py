"""Pipeline orchestrator: ties retrieval + generation together."""

from src.retriever import retrieve
from src.generator import generate


def query_pipeline(query: str, top_k: int = 5, verbose: bool = True) -> str:
    """Full RAG + KG pipeline: retrieve context, generate response.

    Args:
        query: natural language question
        top_k: number of chunks to retrieve
        verbose: print intermediate steps
    """
    if verbose:
        print(f"\nQuery: {query}")
        print("=" * 60)
        print("Retrieving...")

    results = retrieve(query, top_k=top_k)

    if verbose:
        print(f"  Retrieved {len(results)} results")
        for r in results:
            kg = "✓ KG" if r.kg_confirmed else "  vec"
            print(f"    [{kg}] {r.scheme_id} ({r.source_pdf} {r.page_range}) score={r.vector_score:.3f}")
        print("\nGenerating response...")

    response = generate(query, results)

    if verbose:
        print("=" * 60)

    return response
