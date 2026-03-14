"""Data classes for the SamarthSchool RAG + KG pipeline."""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Scheme:
    """A government disability-welfare scheme with structured metadata."""
    id: str
    name: str
    full_name: str
    ministry: str
    level: str  # "central" | "state"
    benefit_type: str  # "financial" | "service" | "insurance" | "equipment"
    benefit_value_inr: str  # human-readable, e.g. "Rs 1,00,000" or "varies"
    frequency: str  # "one-time" | "monthly" | "annual" | "as-needed"
    source_pdf: str
    disability_categories: list[str] = field(default_factory=list)
    states: list[str] = field(default_factory=list)  # empty = all India
    min_age: int = 0
    max_age: int = 100
    max_income_inr: int = 0  # 0 = no income limit
    required_documents: list[str] = field(default_factory=list)
    min_disability_pct: int = 40  # minimum disability % to qualify


@dataclass
class Chunk:
    """A PDF chunk ready for embedding and vector storage."""
    chunk_id: str
    scheme_id: str
    source_pdf: str
    page_start: int
    page_end: int
    text: str
    pdf_bytes: bytes = field(repr=False)


@dataclass
class QueryResult:
    """A single result from hybrid retrieval."""
    scheme_id: str
    scheme_name: str
    chunk_text: str
    vector_score: float
    kg_confirmed: bool  # True if KG eligibility query also matched this scheme
    source_pdf: str
    page_range: str
