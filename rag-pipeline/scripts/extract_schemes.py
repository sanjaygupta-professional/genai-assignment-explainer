#!/usr/bin/env python3.12
"""Extract disability welfare scheme metadata from government PDFs using Gemini 2.0 Flash.

Sends each PDF to Gemini with a structured extraction prompt. Results are saved to
data/extracted_schemes.json for human review before loading into the Knowledge Graph.

Usage:
    python3.12 scripts/extract_schemes.py                  # extract from all PDFs
    python3.12 scripts/extract_schemes.py --pdf compendium_pwd_schemes_2023.pdf  # single PDF
    python3.12 scripts/extract_schemes.py --merge           # merge & deduplicate all extractions
"""

import argparse
import json
import sys
import time
import base64
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from google import genai
from google.genai import types
from src.config import get_api_key, GENERATION_MODEL

ROOT = Path(__file__).resolve().parent.parent
SCHEMES_DIR = ROOT / "data" / "schemes"
OUTPUT_DIR = ROOT / "data"
EXTRACTED_FILE = OUTPUT_DIR / "extracted_schemes.json"

EXTRACTION_PROMPT = """You are an expert on Indian government disability welfare schemes.

Analyze this government PDF document carefully and extract ALL disability welfare schemes mentioned.
For EACH scheme, extract the following structured metadata:

IMPORTANT RULES:
- Extract ONLY schemes that provide benefits to persons with disabilities or their families
- Use the EXACT official scheme name as stated in the document
- For benefit values, use the EXACT amounts mentioned (in Indian Rupees)
- For disability categories, map to these standard RPwD Act 2016 categories:
  visual, hearing, locomotor, intellectual, mental_illness, cerebral_palsy,
  autism, multiple, speech, specific_learning, acid_attack, muscular_dystrophy,
  chronic_neurological, thalassemia, hemophilia, sickle_cell, deaf_blind,
  dwarfism, leprosy_cured, parkinsons, multiple_sclerosis
- If a scheme covers "all disabilities" or "benchmark disability (40%+)", list all 21 categories
- For income limits, convert to annual amount in INR (0 means no income limit)
- If information is not mentioned in the document, use null (not empty string)
- Extract the application URL/portal if mentioned
- Note the source PDF filename

Return a JSON array of scheme objects. Each scheme must have these fields:
{
  "id": "snake_case_short_name",
  "name": "Official English Name",
  "name_hindi": "Official Hindi Name (if available, else null)",
  "full_name": "Complete Official Name",
  "ministry": "Administering Ministry/Department",
  "benefit_type": "financial|equipment|service|insurance|training|loan|housing|multiple",
  "benefit_value_inr": "Exact amount or description (e.g., 'Rs 6,000/year' or 'Up to Rs 10,000')",
  "frequency": "one-time|monthly|annual|as-needed",
  "disability_categories": ["list", "of", "applicable", "categories"],
  "min_disability_pct": 40,
  "min_age": 0,
  "max_age": 0,
  "max_income_inr": 0,
  "required_documents": ["disability_certificate", "income_certificate", "aadhaar", etc.],
  "application_url": "portal URL or null",
  "application_process": "Brief description of how to apply",
  "source_pdf": "filename.pdf"
}"""


def extract_from_pdf(pdf_path: Path, client: genai.Client) -> list[dict]:
    """Send a PDF to Gemini 2.0 Flash and extract scheme metadata."""
    print(f"\n{'='*60}")
    print(f"  Extracting from: {pdf_path.name}")
    print(f"  Size: {pdf_path.stat().st_size / 1024:.0f} KB")
    print(f"{'='*60}")

    pdf_bytes = pdf_path.read_bytes()
    pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")

    try:
        response = client.models.generate_content(
            model=GENERATION_MODEL,
            contents=[
                types.Content(
                    parts=[
                        types.Part(
                            inline_data=types.Blob(
                                mime_type="application/pdf",
                                data=pdf_b64,
                            )
                        ),
                        types.Part(text=EXTRACTION_PROMPT),
                    ]
                )
            ],
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=8192,
            ),
        )

        text = response.text.strip()

        # Clean up markdown code fences if present
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

        schemes = json.loads(text)

        if not isinstance(schemes, list):
            schemes = [schemes]

        # Tag each scheme with source PDF
        for scheme in schemes:
            scheme["source_pdf"] = pdf_path.name

        print(f"  Extracted {len(schemes)} schemes:")
        for s in schemes:
            print(f"    - {s.get('id', '?')}: {s.get('name', '?')}")

        return schemes

    except json.JSONDecodeError as e:
        print(f"  ERROR: Failed to parse JSON response: {e}")
        print(f"  Raw response (first 500 chars): {text[:500]}")
        # Save raw response for debugging
        debug_path = OUTPUT_DIR / f"extraction_debug_{pdf_path.stem}.txt"
        debug_path.write_text(text)
        print(f"  Full response saved to: {debug_path}")
        return []

    except Exception as e:
        print(f"  ERROR: Gemini API call failed: {e}")
        return []


def merge_and_deduplicate(all_schemes: list[dict]) -> list[dict]:
    """Merge schemes from multiple PDFs, deduplicating by ID."""
    seen = {}
    for scheme in all_schemes:
        sid = scheme.get("id", "")
        if sid in seen:
            # Keep the version with more complete data
            existing = seen[sid]
            # Prefer the one with more non-null fields
            existing_score = sum(1 for v in existing.values() if v is not None and v != [])
            new_score = sum(1 for v in scheme.values() if v is not None and v != [])
            if new_score > existing_score:
                # Merge source_pdf references
                sources = set()
                if isinstance(existing.get("source_pdf"), str):
                    sources.add(existing["source_pdf"])
                if isinstance(scheme.get("source_pdf"), str):
                    sources.add(scheme["source_pdf"])
                scheme["source_pdfs"] = sorted(sources)
                seen[sid] = scheme
            else:
                if isinstance(scheme.get("source_pdf"), str):
                    sources = set()
                    if isinstance(existing.get("source_pdfs"), list):
                        sources.update(existing["source_pdfs"])
                    elif isinstance(existing.get("source_pdf"), str):
                        sources.add(existing["source_pdf"])
                    sources.add(scheme["source_pdf"])
                    existing["source_pdfs"] = sorted(sources)
        else:
            seen[sid] = scheme

    merged = list(seen.values())
    print(f"\n  Merged: {len(all_schemes)} extractions → {len(merged)} unique schemes")
    return merged


def main():
    parser = argparse.ArgumentParser(description="Extract scheme metadata from PDFs using Gemini 2.0")
    parser.add_argument("--pdf", help="Extract from a specific PDF filename only")
    parser.add_argument("--merge", action="store_true", help="Merge and deduplicate existing extractions")
    args = parser.parse_args()

    client = genai.Client(api_key=get_api_key())

    if args.merge:
        if EXTRACTED_FILE.exists():
            existing = json.loads(EXTRACTED_FILE.read_text())
            merged = merge_and_deduplicate(existing)
            EXTRACTED_FILE.write_text(json.dumps(merged, indent=2, ensure_ascii=False))
            print(f"Saved {len(merged)} schemes to {EXTRACTED_FILE}")
        else:
            print("No extracted_schemes.json found. Run extraction first.")
        return

    # Determine which PDFs to process
    if args.pdf:
        pdfs = [SCHEMES_DIR / args.pdf]
        if not pdfs[0].exists():
            print(f"PDF not found: {pdfs[0]}")
            sys.exit(1)
    else:
        pdfs = sorted(SCHEMES_DIR.glob("*.pdf"))

    if not pdfs:
        print("No PDFs found in data/schemes/. Run download_schemes.py first.")
        sys.exit(1)

    print(f"Processing {len(pdfs)} PDFs...")

    all_schemes = []

    # Load existing extractions if any
    if EXTRACTED_FILE.exists():
        existing = json.loads(EXTRACTED_FILE.read_text())
        all_schemes.extend(existing)
        print(f"Loaded {len(existing)} existing extractions")

    for pdf in pdfs:
        # Rate limit: wait between API calls
        time.sleep(2.0)
        schemes = extract_from_pdf(pdf, client)
        all_schemes.extend(schemes)

        # Save after each PDF (in case of interruption)
        merged = merge_and_deduplicate(all_schemes)
        EXTRACTED_FILE.write_text(json.dumps(merged, indent=2, ensure_ascii=False))
        print(f"  Progress saved: {len(merged)} unique schemes so far")

    # Final merge
    final = merge_and_deduplicate(all_schemes)
    EXTRACTED_FILE.write_text(json.dumps(final, indent=2, ensure_ascii=False))
    print(f"\n{'='*60}")
    print(f"  DONE: {len(final)} unique schemes extracted")
    print(f"  Saved to: {EXTRACTED_FILE}")
    print(f"{'='*60}")
    print(f"\nNext steps:")
    print(f"  1. Review {EXTRACTED_FILE} for accuracy")
    print(f"  2. Run: python3.12 scripts/ingest.py  (to rebuild KG + vectors)")


if __name__ == "__main__":
    main()
