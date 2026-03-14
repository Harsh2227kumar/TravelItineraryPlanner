"""Week 2: Query preprocessing demo."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.preprocess import preprocess


def run_demo():
    """Run a simple CLI demo for week 2 preprocessing."""
    print("Week 2 - Preprocessing Student Queries")
    print("Type a sentence, or 'exit' to quit.\n")

    while True:
        raw = input("Raw query: ").strip()
        if raw.lower() in {"exit", "quit"}:
            print("Done.")
            break

        cleaned = preprocess(raw)
        print(f"Preprocessed: {cleaned}\n")


if __name__ == "__main__":
    run_demo()
