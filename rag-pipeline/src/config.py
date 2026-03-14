"""Centralized configuration for the SamarthSchool RAG + KG pipeline."""

import os
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
SCHEMES_DIR = DATA_DIR / "schemes"
QDRANT_DIR = DATA_DIR / "qdrant_db"
KUZU_DIR = DATA_DIR / "kuzu_db"

# ── Google AI ──────────────────────────────────────────────────────────
def get_api_key() -> str:
    """Load API key from environment or .env file."""
    key = os.environ.get("GOOGLE_API_KEY")
    if key:
        return key
    env_file = ROOT_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line.startswith("GOOGLE_API_KEY=") and not line.startswith("#"):
                return line.split("=", 1)[1].strip()
    raise RuntimeError(
        "GOOGLE_API_KEY not found. Set it in environment or rag-pipeline/.env"
    )

# ── Model IDs ──────────────────────────────────────────────────────────
EMBEDDING_MODEL = "gemini-embedding-2-preview"  # Gemini Embedding 2
GENERATION_MODEL = "gemini-2.0-flash"

# ── Embedding parameters ──────────────────────────────────────────────
EMBEDDING_DIMS = 768
CHUNK_PAGES = 5        # pages per chunk
CHUNK_OVERLAP = 1      # page overlap between consecutive chunks

# ── Qdrant ─────────────────────────────────────────────────────────────
QDRANT_COLLECTION = "samarthschool_schemes"

# ── Rate limiting ──────────────────────────────────────────────────────
EMBED_DELAY_SEC = 1.5  # seconds between embedding API calls
