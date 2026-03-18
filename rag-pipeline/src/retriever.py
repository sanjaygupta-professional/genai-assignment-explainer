"""Hybrid retriever: combines Knowledge Graph + vector search.

Two retrieval paths:
1. KG path: Extract structured fields from query → Cypher → eligible scheme IDs
2. Vector path: Embed query → Qdrant → semantically similar chunks

Results are merged: KG-confirmed schemes get a score boost.
"""

import json
from google import genai
from google.genai import types
from src.config import get_api_key, GENERATION_MODEL
from src.embedder import embed_query
from src.vectorstore import search as vector_search
from src.knowledge_graph import get_db, query_eligible_schemes, get_scheme_details
from src.schema import QueryResult
import kuzu

_client = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=get_api_key())
    return _client


def extract_query_fields(query: str) -> dict:
    """Use Gemini Flash to extract structured fields from a natural language query.

    Returns dict with optional keys: disability, age, state, income
    """
    client = _get_client()
    response = client.models.generate_content(
        model=GENERATION_MODEL,
        contents=query,
        config=types.GenerateContentConfig(
            system_instruction=(
                "Extract structured fields from a query about Indian disability welfare schemes. "
                "The query may be in English, Hindi, or mixed (Hinglish). "
                "ALWAYS return field values in English, regardless of query language.\n\n"
                "Return a JSON object with these optional keys:\n"
                '- "disability": Map to one of these exact IDs:\n'
                "  visual, hearing, locomotor, intellectual, mental_illness, cerebral_palsy,\n"
                "  autism, multiple, speech, specific_learning, acid_attack, muscular_dystrophy,\n"
                "  chronic_neurological, thalassemia\n\n"
                "  Hindi→English mappings:\n"
                "  दृष्टि/अंधापन/नज़र → visual\n"
                "  श्रवण/बहरापन/कान → hearing\n"
                "  चलने-फिरने/शारीरिक/लोकोमोटर → locomotor\n"
                "  बौद्धिक/मानसिक मंदता → intellectual\n"
                "  मानसिक बीमारी/मनोरोग → mental_illness\n"
                "  सेरेब्रल पाल्सी → cerebral_palsy\n"
                "  ऑटिज़्म/स्वलीनता → autism\n"
                "  बहु-विकलांगता → multiple\n"
                "  वाक्/बोलने → speech\n"
                "  डिस्लेक्सिया/अधिगम → specific_learning\n"
                "  तेज़ाब → acid_attack\n"
                "  मस्कुलर डिस्ट्रॉफी → muscular_dystrophy\n"
                "  पार्किंसन/तंत्रिका → chronic_neurological\n"
                "  थैलेसीमिया/रक्त → thalassemia\n\n"
                '- "age": integer age (e.g., "उम्र 8 साल" → 8, "12 years old" → 12)\n'
                '- "state": Indian state name IN ENGLISH '
                '(e.g., "कर्नाटक" → "Karnataka", "उत्तर प्रदेश" → "Uttar Pradesh")\n'
                '- "income": annual income in INR as integer '
                '(e.g., "1.2 लाख" → 120000, "₹2,50,000" → 250000)\n\n'
                "Only include keys that are explicitly mentioned or clearly implied. "
                "Return {} if no structured fields found. "
                "Return ONLY valid JSON, no explanation."
            ),
            temperature=0.0,
        ),
    )
    text = response.text.strip()
    # Clean potential markdown wrapping
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}


def retrieve(query: str, top_k: int = 5) -> list[QueryResult]:
    """Hybrid retrieval: KG eligibility + vector similarity.

    Steps:
    1. Extract structured fields from query via Gemini Flash
    2. Query KG for eligible scheme IDs
    3. Embed the query text
    4. Search Qdrant (optionally filtered to KG-eligible schemes)
    5. Merge and rank results
    """
    # Step 1: Parse query into structured fields
    fields = extract_query_fields(query)
    print(f"  Extracted fields: {fields}")

    # Step 2: KG eligibility query
    kg_scheme_ids = set()
    kg_schemes = {}
    if any(k in fields for k in ("disability", "age", "state", "income")):
        db = get_db()
        conn = kuzu.Connection(db)
        kg_results = query_eligible_schemes(
            conn,
            disability=fields.get("disability"),
            age=fields.get("age"),
            state=fields.get("state"),
            max_income=fields.get("income"),
        )
        for r in kg_results:
            kg_scheme_ids.add(r["id"])
            kg_schemes[r["id"]] = r
        print(f"  KG eligible schemes: {[r['name'] for r in kg_results]}")

    # Step 3: Embed query
    query_vector = embed_query(query)

    # Step 4: Vector search
    # If KG found schemes, first search within those; also search broadly
    results = []
    seen_chunks = set()

    if kg_scheme_ids:
        # Filtered search — only KG-eligible schemes
        kg_results = vector_search(query_vector, top_k=top_k, scheme_ids=list(kg_scheme_ids))
        for hit in kg_results:
            if hit["chunk_id"] not in seen_chunks:
                seen_chunks.add(hit["chunk_id"])
                results.append(QueryResult(
                    scheme_id=hit["scheme_id"],
                    scheme_name=kg_schemes.get(hit["scheme_id"], {}).get("name", hit["scheme_id"]),
                    chunk_text=hit["text"],
                    vector_score=hit["score"] + 0.1,  # KG-confirmed boost
                    kg_confirmed=True,
                    source_pdf=hit["source_pdf"],
                    page_range=hit["page_range"],
                ))

    # Broad search (no filter)
    broad_results = vector_search(query_vector, top_k=top_k)
    for hit in broad_results:
        if hit["chunk_id"] not in seen_chunks:
            seen_chunks.add(hit["chunk_id"])
            is_kg = hit["scheme_id"] in kg_scheme_ids
            results.append(QueryResult(
                scheme_id=hit["scheme_id"],
                scheme_name=kg_schemes.get(hit["scheme_id"], {}).get("name", hit["scheme_id"]),
                chunk_text=hit["text"],
                vector_score=hit["score"] + (0.1 if is_kg else 0.0),
                kg_confirmed=is_kg,
                source_pdf=hit["source_pdf"],
                page_range=hit["page_range"],
            ))

    # Step 5: Sort by score (KG-confirmed gets boost)
    results.sort(key=lambda r: r.vector_score, reverse=True)
    return results[:top_k]
