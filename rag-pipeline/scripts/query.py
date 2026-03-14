#!/usr/bin/env python3.12
"""Query the SamarthSchool RAG + KG pipeline.

Usage:
    python3.12 scripts/query.py "What schemes are available for a child with autism?"
    python3.12 scripts/query.py --interactive     # REPL mode
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.pipeline import query_pipeline


def main():
    parser = argparse.ArgumentParser(description="Query SamarthSchool pipeline")
    parser.add_argument("query", nargs="?", help="Query string")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="Interactive REPL mode")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results")
    args = parser.parse_args()

    if args.interactive:
        print("SamarthSchool RAG + KG Pipeline — Interactive Mode")
        print("Type your question (or 'quit' to exit)")
        print("-" * 50)
        while True:
            try:
                query = input("\n> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break
            if not query or query.lower() in ("quit", "exit", "q"):
                print("Goodbye!")
                break
            response = query_pipeline(query, top_k=args.top_k)
            print(f"\n{response}")
    elif args.query:
        response = query_pipeline(args.query, top_k=args.top_k)
        print(f"\n{response}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
