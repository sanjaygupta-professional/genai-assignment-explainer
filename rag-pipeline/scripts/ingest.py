#!/usr/bin/env python3.12
"""Ingest: embed PDFs into Qdrant + build Knowledge Graph.

Usage:
    python3.12 scripts/ingest.py              # full ingestion
    python3.12 scripts/ingest.py --text-only  # use text embeddings (faster, no PDF upload)
    python3.12 scripts/ingest.py --kg-only    # rebuild KG only (no embedding)
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.chunker import chunk_all_pdfs
from src.embedder import embed_pdf_chunk, embed_text
from src.vectorstore import create_collection, upsert_chunks, get_collection_info
from src.knowledge_graph import populate_graph


def ingest(text_only: bool = False, kg_only: bool = False) -> None:
    # ── Step 1: Knowledge Graph ────────────────────────────────────
    print("Building Knowledge Graph...")
    nodes, rels = populate_graph()
    print(f"  KG: {nodes} nodes, {rels} relationships")

    if kg_only:
        print("Done (KG only).")
        return

    # ── Step 2: Chunk PDFs ─────────────────────────────────────────
    print("\nChunking PDFs...")
    chunks = chunk_all_pdfs()
    print(f"  Total: {len(chunks)} chunks")

    # ── Step 3: Embed chunks ───────────────────────────────────────
    print("\nEmbedding chunks...")
    vectors = []
    chunk_ids = []
    payloads = []

    for i, chunk in enumerate(chunks):
        progress = f"[{i + 1}/{len(chunks)}]"
        try:
            if text_only:
                vec = embed_text(chunk.text)
            else:
                vec = embed_pdf_chunk(chunk.pdf_bytes)
            vectors.append(vec)
            chunk_ids.append(chunk.chunk_id)
            payloads.append({
                "scheme_id": chunk.scheme_id,
                "source_pdf": chunk.source_pdf,
                "page_range": f"p{chunk.page_start}-{chunk.page_end}",
                "text": chunk.text[:2000],  # truncate for payload storage
            })
            print(f"  {progress} {chunk.chunk_id} ({len(vec)}d)")
        except Exception as e:
            print(f"  {progress} FAILED {chunk.chunk_id}: {e}")
            continue

    # ── Step 4: Store in Qdrant ────────────────────────────────────
    print(f"\nStoring {len(vectors)} vectors in Qdrant...")
    create_collection()
    upsert_chunks(chunk_ids, vectors, payloads)

    info = get_collection_info()
    print(f"  Collection '{info['name']}': {info['points_count']} points")
    print("\nIngestion complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest PDFs into RAG pipeline")
    parser.add_argument("--text-only", action="store_true",
                        help="Use text embeddings instead of PDF embeddings (faster)")
    parser.add_argument("--kg-only", action="store_true",
                        help="Only rebuild the Knowledge Graph")
    args = parser.parse_args()
    ingest(text_only=args.text_only, kg_only=args.kg_only)
