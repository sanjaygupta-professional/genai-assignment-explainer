#!/usr/bin/env python3.12
"""Pre-scripted demo queries showcasing the RAG + KG pipeline.

Demonstrates:
1. Simple eligibility query (English)
2. Multi-criteria KG filtering (disability + age + state + income)
3. Hindi multilingual query
4. Out-of-scope guardrails
5. Graph exploration query
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.pipeline import query_pipeline

DEMO_QUERIES = [
    {
        "label": "1. Simple eligibility query (English)",
        "query": "What government schemes are available for children with autism in India?",
    },
    {
        "label": "2. Multi-criteria KG query (disability + age + state + income)",
        "query": (
            "My daughter is 12 years old with locomotor disability. "
            "We live in Karnataka and our family income is Rs 1.2 lakh per year. "
            "What schemes can she apply for?"
        ),
    },
    {
        "label": "3. Hindi multilingual query",
        "query": "मेरे बेटे को सेरेब्रल पाल्सी है, उम्र 8 साल। कौन सी सरकारी योजनाएं उपलब्ध हैं?",
    },
    {
        "label": "4. Out-of-scope query (guardrails test)",
        "query": "What is the best restaurant in Mumbai?",
    },
    {
        "label": "5. Graph exploration — all schemes for hearing disability",
        "query": "Show me all government schemes that cover hearing impairment disability. What are the benefits and documents required?",
    },
]


def main():
    print("=" * 70)
    print("  SamarthSchool RAG + Knowledge Graph Pipeline — DEMO")
    print("=" * 70)

    for demo in DEMO_QUERIES:
        print(f"\n{'─' * 70}")
        print(f"  {demo['label']}")
        print(f"{'─' * 70}")

        response = query_pipeline(demo["query"], top_k=5)
        print(f"\n{response}")
        print()


if __name__ == "__main__":
    main()
