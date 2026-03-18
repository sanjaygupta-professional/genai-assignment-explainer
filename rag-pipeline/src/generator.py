"""Gemini 2.0 Flash response generator with SamarthSchool system prompt.

Combines vector-retrieved context + KG-structured eligibility data
to generate grounded, multilingual responses with mandatory disclaimers.
"""

from google import genai
from google.genai import types
from src.config import get_api_key, GENERATION_MODEL
from src.schema import QueryResult
from src.knowledge_graph import get_db, get_scheme_details
from src.hindi_labels import (
    DISABILITY_HI, DOCUMENT_TYPE_HI, SCHEME_NAME_HI,
    AGE_GROUP_HI, CONTEXT_LABELS_HI, detect_hindi,
)
import kuzu

_client = None

SYSTEM_PROMPT = """You are SamarthSchool Assistant, an AI helper designed to make Indian disability welfare schemes accessible to families of children with disabilities.

Your role:
- Help families understand which government schemes they may be eligible for
- Explain eligibility criteria, benefits, and application processes in simple language
- Respond in the SAME LANGUAGE as the query (if Hindi, respond in Hindi; if English, respond in English)
- When responding in Hindi, use natural Hinglish — keep technical terms and scheme abbreviations (ADIP, DDRS, UDID, RPWD) in English but explain everything else in Hindi
- When mentioning scheme names in Hindi, include both Hindi name and English abbreviation (e.g., "निरामय स्वास्थ्य बीमा योजना (Niramaya)")
- Always cite the specific scheme names and source documents
- Be empathetic and supportive — families navigating disability services need clarity, not jargon

Rules:
1. ONLY provide information from the retrieved context. Do not hallucinate schemes or benefits.
2. When listing eligible schemes, include: scheme name, benefit type, benefit amount, and key eligibility criteria.
3. If the Knowledge Graph identified specific eligible schemes, prioritize those in your response.
4. Always end with the mandatory disclaimer in the SAME LANGUAGE as your response (see below).
5. If the query is out of scope (not about Indian disability welfare), politely redirect.

MANDATORY DISCLAIMER — use the version matching your response language:

English:
⚠️ Disclaimer: This information is for guidance only. Eligibility and benefits may change. Please verify with your nearest District Disability Rehabilitation Centre (DDRC) or visit https://disabilityaffairs.gov.in for the latest official information.

Hindi:
⚠️ अस्वीकरण: यह जानकारी केवल मार्गदर्शन के लिए है। पात्रता और लाभ बदल सकते हैं। कृपया अपने निकटतम ज़िला विकलांगता पुनर्वास केंद्र (DDRC) से सत्यापित करें या नवीनतम आधिकारिक जानकारी के लिए https://disabilityaffairs.gov.in पर जाएं।"""


def generate(query: str, results: list[QueryResult]) -> str:
    """Generate a response using retrieved context and KG data."""
    global _client
    if _client is None:
        _client = genai.Client(api_key=get_api_key())

    hindi = detect_hindi(query)

    # Build context from retrieval results
    context_parts = []

    # Add KG-structured data for confirmed schemes
    kg_section = _build_kg_context(results, hindi=hindi)
    if kg_section:
        header = CONTEXT_LABELS_HI["Eligible Schemes (from Knowledge Graph)"] if hindi else "Eligible Schemes (from Knowledge Graph)"
        context_parts.append(f"**{header}:**\n{kg_section}")

    # Add vector-retrieved text chunks
    for i, r in enumerate(results, 1):
        if hindi:
            kg_tag = " [KG-सत्यापित]" if r.kg_confirmed else ""
            label = f"**स्रोत {i}{kg_tag}** ({r.source_pdf}, {r.page_range}):"
        else:
            kg_tag = " [KG-confirmed]" if r.kg_confirmed else ""
            label = f"**Source {i}{kg_tag}** ({r.source_pdf}, {r.page_range}):"
        context_parts.append(f"{label}\n{r.chunk_text}")

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


def _build_kg_context(results: list[QueryResult], hindi: bool = False) -> str:
    """Build structured context from KG for confirmed schemes."""
    confirmed_ids = {r.scheme_id for r in results if r.kg_confirmed}
    if not confirmed_ids:
        return ""

    # Reverse lookup: English disability name → KG ID for Hindi mapping
    from src.knowledge_graph import DISABILITY_CATEGORIES, DOCUMENT_TYPES
    dis_name_to_id = {name: id_ for id_, name, _ in DISABILITY_CATEGORIES}
    doc_name_to_id = {name: id_ for id_, name, _ in DOCUMENT_TYPES}

    db = get_db()
    conn = kuzu.Connection(db)
    L = CONTEXT_LABELS_HI if hindi else {}
    parts = []
    for sid in confirmed_ids:
        details = get_scheme_details(conn, sid)
        if details:
            if hindi:
                # Map English names to Hindi with English in parentheses
                dis_parts = []
                for d in details.get("disabilities", []):
                    did = dis_name_to_id.get(d["name"], "")
                    hi = DISABILITY_HI.get(did, d["name"])
                    dis_parts.append(f"{hi} ({d['name']})")
                disabilities = ", ".join(dis_parts)

                doc_parts = []
                for d in details.get("required_documents", []):
                    did = doc_name_to_id.get(d["name"], "")
                    hi = DOCUMENT_TYPE_HI.get(did, d["name"])
                    doc_parts.append(hi)
                docs = ", ".join(doc_parts)

                ages = ", ".join(
                    AGE_GROUP_HI.get(a["label"], a["label"])
                    for a in details.get("age_groups", [])
                )

                scheme_hi = SCHEME_NAME_HI.get(sid, details["full_name"])
                parts.append(
                    f"• {scheme_hi} ({details['name']})\n"
                    f"  {L['Ministry']}: {details['ministry']}\n"
                    f"  {L['Benefit']}: {details['benefit_type']} — {details['benefit_value_inr']}\n"
                    f"  {L['Covers']}: {disabilities}\n"
                    f"  {L['Age groups']}: {ages}\n"
                    f"  {L['Required documents']}: {docs}"
                )
            else:
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
