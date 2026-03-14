"""Gemini 2.0 Flash response generator with SamarthSchool system prompt.

Combines vector-retrieved context + KG-structured eligibility data
to generate grounded, multilingual responses with mandatory disclaimers.
"""

from google import genai
from google.genai import types
from src.config import get_api_key, GENERATION_MODEL
from src.schema import QueryResult
from src.knowledge_graph import get_db, get_scheme_details
import kuzu

_client = None

SYSTEM_PROMPT = """You are SamarthSchool Assistant, an AI helper designed to make Indian disability welfare schemes accessible to families of children with disabilities.

Your role:
- Help families understand which government schemes they may be eligible for
- Explain eligibility criteria, benefits, and application processes in simple language
- Respond in the SAME LANGUAGE as the query (if Hindi, respond in Hindi; if English, respond in English)
- Always cite the specific scheme names and source documents
- Be empathetic and supportive — families navigating disability services need clarity, not jargon

Rules:
1. ONLY provide information from the retrieved context. Do not hallucinate schemes or benefits.
2. When listing eligible schemes, include: scheme name, benefit type, benefit amount, and key eligibility criteria.
3. If the Knowledge Graph identified specific eligible schemes, prioritize those in your response.
4. Always end with the mandatory disclaimer (see below).
5. If the query is out of scope (not about Indian disability welfare), politely redirect.

MANDATORY DISCLAIMER (include at the end of EVERY response):
---
⚠️ Disclaimer: This information is for guidance only. Eligibility and benefits may change. Please verify with your nearest District Disability Rehabilitation Centre (DDRC) or visit https://disabilityaffairs.gov.in for the latest official information.
---"""


def generate(query: str, results: list[QueryResult]) -> str:
    """Generate a response using retrieved context and KG data."""
    global _client
    if _client is None:
        _client = genai.Client(api_key=get_api_key())

    # Build context from retrieval results
    context_parts = []

    # Add KG-structured data for confirmed schemes
    kg_section = _build_kg_context(results)
    if kg_section:
        context_parts.append(f"**Eligible Schemes (from Knowledge Graph):**\n{kg_section}")

    # Add vector-retrieved text chunks
    for i, r in enumerate(results, 1):
        kg_tag = " [KG-confirmed]" if r.kg_confirmed else ""
        context_parts.append(
            f"**Source {i}{kg_tag}** ({r.source_pdf}, {r.page_range}):\n{r.chunk_text}"
        )

    context = "\n\n---\n\n".join(context_parts)

    response = _client.models.generate_content(
        model=GENERATION_MODEL,
        contents=f"Query: {query}\n\nRetrieved Context:\n{context}",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.3,
            max_output_tokens=2048,
        ),
    )
    return response.text


def _build_kg_context(results: list[QueryResult]) -> str:
    """Build structured context from KG for confirmed schemes."""
    confirmed_ids = {r.scheme_id for r in results if r.kg_confirmed}
    if not confirmed_ids:
        return ""

    db = get_db()
    conn = kuzu.Connection(db)
    parts = []
    for sid in confirmed_ids:
        details = get_scheme_details(conn, sid)
        if details:
            disabilities = ", ".join(d["name"] for d in details.get("disabilities", []))
            docs = ", ".join(d["name"] for d in details.get("required_documents", []))
            ages = ", ".join(a["label"] for a in details.get("age_groups", []))
            parts.append(
                f"• {details['full_name']} ({details['name']})\n"
                f"  Ministry: {details['ministry']}\n"
                f"  Benefit: {details['benefit_type']} — {details['benefit_value_inr']}\n"
                f"  Covers: {disabilities}\n"
                f"  Age groups: {ages}\n"
                f"  Required documents: {docs}"
            )
    return "\n\n".join(parts)
