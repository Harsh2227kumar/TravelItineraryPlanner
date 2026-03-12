"""
Unit tests for the fallback handler.

Run with: python -m pytest tests/test_fallback.py -v
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.fallback import (  # noqa: E402
    handle_response,
    format_suggestions_text,
    format_handover_text,
)


class TestFallbackHandler:
    """Test suite for the fallback system."""

    def test_high_confidence_returns_answer(self):
        """Scores above 0.3 should return type 'answer'."""
        response = handle_response("test", "Answer text", 0.8)
        assert response["type"] == "answer"
        assert response["answer"] == "Answer text"

    def test_medium_confidence_returns_soft_fallback(self):
        """Scores between 0.2 and 0.3 should return soft fallback."""
        response = handle_response("test", "Answer text", 0.25)
        assert response["type"] == "fallback_soft"
        assert "clarification" in response

    def test_low_confidence_returns_hard_fallback(self):
        """Scores below 0.2 should return hard fallback."""
        response = handle_response("test", "Answer text", 0.1)
        assert response["type"] == "fallback_hard"
        assert "advisor" in response
        assert "email" in response["advisor"]

    def test_soft_fallback_with_suggestions(self):
        """Soft fallback should call get_top_n and include suggestions."""
        mock_top_n = lambda q, n: [("Q1?", "A1", 0.3), ("Q2?", "A2", 0.2)]
        response = handle_response("test", "Answer", 0.25, get_top_n_fn=mock_top_n)
        assert len(response["suggestions"]) == 2

    def test_format_suggestions_text(self):
        """Suggestions should format as numbered list."""
        suggestions = [{"question": "Q1?"}, {"question": "Q2?"}]
        text = format_suggestions_text(suggestions)
        assert "1." in text
        assert "2." in text

    def test_format_handover_text(self):
        """Handover text should include contact info."""
        text = format_handover_text()
        assert "Email" in text
        assert "Phone" in text
