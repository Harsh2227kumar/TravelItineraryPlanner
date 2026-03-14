"""Week 1: Basic FAQ responder (keyword matching)."""

import os
import string
import sys
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data import load_faqs


class KeywordMatcher:
    """Simple keyword-overlap matcher for FAQ questions."""

    def __init__(self, faqs: List[Dict[str, str]]):
        """Store FAQ records for matching."""
        self.faqs = faqs

    @staticmethod
    def _extract_keywords(text: str) -> set:
        """Convert text to lowercase keyword set."""
        cleaned = text.lower().translate(str.maketrans("", "", string.punctuation))
        return set(cleaned.split())

    def get_answer(self, query: str) -> Tuple[str, float]:
        """Return best matching answer and confidence."""
        query_keywords = self._extract_keywords(query)
        if not query_keywords:
            return "Please ask a question about the college.", 0.0

        best_answer = "Sorry, I don't have an answer for that question yet."
        best_score = 0.0

        for faq in self.faqs:
            faq_keywords = self._extract_keywords(faq["question"])
            overlap = query_keywords & faq_keywords
            score = len(overlap) / len(query_keywords)
            if score > best_score:
                best_score = score
                best_answer = faq["answer"]

        return best_answer, round(best_score, 2)


def run_demo():
    """Run a simple CLI demo for week 1 keyword matching."""
    faqs = load_faqs()
    bot = KeywordMatcher(faqs)

    print("Week 1 - Basic FAQ Responder")
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
