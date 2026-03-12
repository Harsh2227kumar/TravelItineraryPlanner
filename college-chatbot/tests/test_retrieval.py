"""
Unit tests for the TF-IDF retrieval engine.

Run with: python -m pytest tests/test_retrieval.py -v
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.retrieval import TFIDFRetriever  # noqa: E402

SAMPLE_FAQS = [
    {"question": "What are the college timings?", "answer": "8:00 AM to 5:00 PM.", "category": "timings"},
    {"question": "What is the fee for B.Tech?", "answer": "₹80,000 per year.", "category": "fees"},
    {"question": "What are the hostel facilities?", "answer": "Separate boys' and girls' hostels.", "category": "hostel"},
    {"question": "When are the semester exams?", "answer": "May and December.", "category": "exams"},
    {"question": "How do I contact the admission office?", "answer": "Call 011-2345-6789.", "category": "contacts"},
]


class TestTFIDFRetriever:
    """Test suite for the TF-IDF retrieval engine."""

    def setup_method(self):
        self.retriever = TFIDFRetriever(SAMPLE_FAQS)

    def test_exact_match_high_score(self):
        """Exact question should return high confidence answer."""
        answer, score = self.retriever.get_answer("What are the college timings?")
        assert "8:00 AM" in answer
        assert score > 0.5

    def test_partial_match(self):
        """Partial query should find relevant FAQ."""
        answer, score = self.retriever.get_answer("college timings")
        assert "8:00 AM" in answer
        assert score > 0.0

    def test_synonym_match(self):
        """Synonym query should match via synonym expansion."""
        answer, score = self.retriever.get_answer("tuition payment cost")
        assert score > 0.0

    def test_empty_query(self):
        """Empty query should return prompt message."""
        answer, score = self.retriever.get_answer("")
        assert score == 0.0

    def test_score_range(self):
        """Score should be between 0 and 1."""
        _, score = self.retriever.get_answer("hostel")
        assert 0.0 <= score <= 1.0

    def test_top_n_returns_list(self):
        """get_top_n should return a list of tuples."""
        results = self.retriever.get_top_n("college", n=3)
        assert isinstance(results, list)
        for item in results:
            assert len(item) == 3  # (question, answer, score)

    def test_top_n_empty_query(self):
        """get_top_n with empty query should return empty list."""
        results = self.retriever.get_top_n("", n=3)
        assert results == []
