"""
Unit tests for the KeywordMatcher engine.

Run with: python -m pytest tests/ -v
"""

import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.matcher import KeywordMatcher  # noqa: E402

# Sample FAQ data for testing
SAMPLE_FAQS = [
    {
        "question": "What are the college timings?",
        "answer": "College timings are 8:00 AM to 5:00 PM.",
        "category": "timings",
    },
    {
        "question": "What is the fee for B.Tech?",
        "answer": "B.Tech fee is ₹80,000 per year.",
        "category": "fees",
    },
    {
        "question": "What are the hostel facilities?",
        "answer": "The college has separate boys' and girls' hostels.",
        "category": "hostel",
    },
    {
        "question": "When are the semester exams?",
        "answer": "End-semester exams are in May and December.",
        "category": "exams",
    },
    {
        "question": "How do I contact the admission office?",
        "answer": "Call 011-2345-6789.",
        "category": "contacts",
    },
]


class TestKeywordMatcher:
    """Test suite for the KeywordMatcher class."""

    def setup_method(self):
        """Create a matcher instance before each test."""
        self.matcher = KeywordMatcher(SAMPLE_FAQS)

    def test_exact_match_returns_correct_answer(self):
        """An exact question should return the corresponding answer."""
        answer, score = self.matcher.get_answer("What are the college timings?")
        assert "8:00 AM" in answer
        assert score > 0.5

    def test_partial_match_returns_relevant_answer(self):
        """A partial query should still find the closest FAQ."""
        answer, score = self.matcher.get_answer("college timings")
        assert "8:00 AM" in answer
        assert score > 0.0

    def test_fee_query_matches_fee_faq(self):
        """A fee-related query should match the fee FAQ."""
        answer, score = self.matcher.get_answer("fee for B.Tech")
        assert "₹80,000" in answer

    def test_no_match_returns_fallback(self):
        """A completely unrelated query should return the fallback message."""
        answer, score = self.matcher.get_answer("xyzzy gibberish foobar")
        assert score == 0.0
        assert "Sorry" in answer

    def test_empty_query_returns_prompt(self):
        """An empty query should return a helpful prompt."""
        answer, score = self.matcher.get_answer("")
        assert score == 0.0
        assert "Please" in answer

    def test_score_is_between_0_and_1(self):
        """Confidence score should always be in [0, 1]."""
        answer, score = self.matcher.get_answer("hostel facilities")
        assert 0.0 <= score <= 1.0
