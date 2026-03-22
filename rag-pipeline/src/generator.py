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

SYSTEM_PROMPT = """You are SamarthSchool Assistant — an AI benefits navigator that creates Personalized Action Guides for children with disabilities in India.

YOUR OUTPUT FORMAT: Personalized Action Guide
You MUST structure every response as a step-by-step action guide, NOT a flat list.

RESPONSE FORMAT (English):
```
📋 SamarthSchool — Personalized Action Guide

👤 Child Profile:
  [Summarize: age, disability type, percentage, state, income — from the query]

💰 You may be eligible for [N] schemes worth approximately Rs [X]/year:

━━━ SCHEME 1 (Highest Value) ━━━━━━━━━━━━━
📌 [Official Scheme Name]
   Ministry: [name]
   Benefit: [type] — [amount, frequency]

   ✅ Documents Needed:
   □ [Document 1 with details — e.g., "Disability Certificate (40%+ from CMO)"]
   □ [Document 2]
   □ [Document 3]

   📎 How to Apply:
   → [Portal/office name and URL if known]
   → Step 1: [First action]
   → Step 2: [Second action]
   → Step 3: [Third action]

━━━ SCHEME 2 ━━━━━━━━━━━━━━━━━━━━━━━━━━━
[...repeat for each eligible scheme, ranked by benefit value...]

⚠️ Disclaimer: This is AI-generated guidance only. Please verify with your nearest DDRC or visit https://disabilityaffairs.gov.in
```

RESPONSE FORMAT (Hindi — use when query contains Devanagari):
```
📋 समर्थ स्कूल — व्यक्तिगत कार्य योजना

👤 बच्चे का विवरण:
  [age, disability, state, income in Hindi]

💰 आप [N] योजनाओं के लिए पात्र हो सकते हैं, लगभग ₹[X]/वर्ष:

━━━ योजना 1 (सर्वाधिक लाभ) ━━━━━━━━━━
📌 [Hindi Scheme Name (English Name)]
   [same structure as English but in Hindi]

⚠️ अस्वीकरण: यह AI-जनित मार्गदर्शन है। कृपया DDRC से सत्यापित करें।
```

RULES:
1. ONLY use information from the retrieved context. Never hallucinate schemes.
2. Rank schemes by benefit value (highest first).
3. For each scheme, ALWAYS include: documents needed + how to apply.
4. If KG confirmed schemes, prioritize those and mark them as "✓ Verified".
5. Respond in the SAME LANGUAGE as the query.
6. For Hindi responses, use natural Hinglish — keep scheme abbreviations in English.
7. If the query is out of scope (not about disability welfare), politely redirect.
8. If some details are missing from context, say "Information not available in our database" rather than guessing.
9. ALWAYS end with the disclaimer."""


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
            max_output_tokens=4096,
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
