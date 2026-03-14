"""Gemini Embedding 2 wrapper for PDF and text embedding.

Gemini Embedding 2 (gemini-embedding-exp-03-07) natively embeds PDFs —
no OCR or text extraction needed for the embedding step. We use
task_type to distinguish document indexing vs query embedding.
"""

import time
import base64
from google import genai
from google.genai import types
from src.config import get_api_key, EMBEDDING_MODEL, EMBEDDING_DIMS, EMBED_DELAY_SEC

_client = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=get_api_key())
    return _client


def embed_pdf_chunk(pdf_bytes: bytes) -> list[float]:
    """Embed a raw PDF chunk using Gemini Embedding 2.

    Uses RETRIEVAL_DOCUMENT task type and 768-dim output (Matryoshka).
    """
    client = _get_client()
    b64 = base64.standard_b64encode(pdf_bytes).decode("utf-8")

    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=types.Content(
            parts=[types.Part(inline_data=types.Blob(mime_type="application/pdf", data=b64))]
        ),
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=EMBEDDING_DIMS,
        ),
    )
    time.sleep(EMBED_DELAY_SEC)
    return result.embeddings[0].values


def embed_text(text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> list[float]:
    """Embed text using Gemini Embedding 2.

    Used for both document text chunks and queries.
    """
    client = _get_client()
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=EMBEDDING_DIMS,
        ),
    )
    time.sleep(EMBED_DELAY_SEC)
    return result.embeddings[0].values


def embed_query(text: str) -> list[float]:
    """Embed a search query. Uses RETRIEVAL_QUERY task type."""
    return embed_text(text, task_type="RETRIEVAL_QUERY")
