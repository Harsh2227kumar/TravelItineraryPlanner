"""Week 3: Synonym-aware query normalization demo."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.preprocessor import preprocess
from src.core.synonyms import apply_synonyms


def run_demo():
    """Run a simple CLI demo for week 3 synonym mapping."""
    print("Week 3 - Synonym-Aware FAQ Bot")
    print("Type a sentence, or 'exit' to quit.\n")

    while True:
        raw = input("Raw query: ").strip()
        if raw.lower() in {"exit", "quit"}:
            print("Done.")
            break

        cleaned = preprocess(raw)
        expanded = apply_synonyms(cleaned)
        print(f"Preprocessed: {cleaned}")
        print(f"Synonym mapped: {expanded}\n")


if __name__ == "__main__":
    run_demo()
