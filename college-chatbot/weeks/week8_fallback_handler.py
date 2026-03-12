"""Week 8: Fallback and handover demo."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.fallback import handle_response


def run_demo():
    """Show answer, soft fallback, and hard fallback cases."""
    print("Week 8 - Fallbacks and Handover\n")

    cases = [
        ("Known question", "Known answer", 0.78),
        ("Partially matched", "Possible answer", 0.25),
        ("Unknown domain", "", 0.05),
    ]

    for query, answer, score in cases:
        result = handle_response(query=query, answer=answer, score=score)
        print(f"Query: {query}")
        print(f"Response type: {result['type']}")
        print(f"Payload: {result}\n")


if __name__ == "__main__":
    run_demo()
