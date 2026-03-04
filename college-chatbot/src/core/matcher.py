"""
Keyword-matching engine.

Uses keyword overlap between the user query and stored FAQ questions
to find the best match. This is the simplest retrieval strategy and
serves as the baseline engine.
"""

import string
from typing import List, Dict, Tuple

from src.config import FALLBACK_ANSWER, EMPTY_QUERY_MSG


class KeywordMatcher:
    """
    FAQ matching engine based on keyword overlap.

    Compares the set of keywords in the user's query against each FAQ
    question and returns the one with the highest overlap ratio.
    """

    def __init__(self, faqs: List[Dict[str, str]]):
        """
        Initialize the matcher with a list of FAQ entries.

        Args:
            faqs: List of dicts with 'question' and 'answer' keys.
        """
        self.faqs = faqs

    @staticmethod
    def _extract_keywords(text: str) -> set:
        """Convert text to a set of lowercase keywords, stripping punctuation."""
        cleaned = text.lower().translate(str.maketrans("", "", string.punctuation))
        return set(cleaned.split())

    def get_answer(self, query: str) -> Tuple[str, float]:
        """
        Find the best matching FAQ answer for the given query.

        Args:
            query: The student's question as a raw string.

        Returns:
            Tuple of (answer_text, confidence_score).
            Score is the fraction of query keywords found in the FAQ question.
        """
        query_keywords = self._extract_keywords(query)
        if not query_keywords:
            return EMPTY_QUERY_MSG, 0.0

        best_answer = FALLBACK_ANSWER
        best_score = 0.0

        for faq in self.faqs:
            faq_keywords = self._extract_keywords(faq["question"])
            overlap = query_keywords & faq_keywords
            score = len(overlap) / len(query_keywords)

            if score > best_score:
                best_score = score
                best_answer = faq["answer"]

        return best_answer, round(best_score, 2)
