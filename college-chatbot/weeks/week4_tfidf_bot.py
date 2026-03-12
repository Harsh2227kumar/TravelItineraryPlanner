"""Week 4: TF-IDF FAQ retrieval demo."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.loader import load_faqs
from src.core.retrieval import TFIDFRetriever


def run_demo():
    """Run a simple CLI demo for week 4 TF-IDF retrieval."""
    faqs = load_faqs()
    bot = TFIDFRetriever(faqs)

    print("Week 4 - FAQ Retrieval with TF-IDF")
    print("Type a question, or 'exit' to quit.\n")

    while True:
        query = input("You: ").strip()
        if query.lower() in {"exit", "quit"}:
            print("Bot: Goodbye!")
            break

        answer, score = bot.get_answer(query)
        print(f"Bot: {answer}")
        print(f"Confidence: {score:.2f}\n")


if __name__ == "__main__":
    run_demo()
