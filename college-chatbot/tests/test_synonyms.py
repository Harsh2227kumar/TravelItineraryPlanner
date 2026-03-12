"""
Unit tests for the synonym module.

Run with: python -m pytest tests/test_synonyms.py -v
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.synonyms import apply_synonyms  # noqa: E402


class TestSynonyms:
    """Tests for synonym expansion."""

    def test_fees_synonyms(self):
        """Tuition/payment variants should map to 'fees'."""
        result = apply_synonyms("tuition payment schedule")
        assert "fees" in result

    def test_exam_synonyms(self):
        """Test/assessment should map to 'exam'."""
        result = apply_synonyms("test assessment date")
        assert "exam" in result

    def test_hostel_synonyms(self):
        """Accommodation/dorm should map to 'hostel'."""
        result = apply_synonyms("accommodation dorm rules")
        assert "hostel" in result

    def test_no_change_for_unknown_words(self):
        """Unknown words should pass through unchanged."""
        result = apply_synonyms("hello world")
        assert result == "hello world"

    def test_empty_string(self):
        """Empty input should return empty output."""
        assert apply_synonyms("") == ""

    def test_contact_synonyms(self):
        """Office/helpdesk should map to 'contact'."""
        result = apply_synonyms("office helpdesk number")
        assert "contact" in result

    def test_placement_synonyms(self):
        """Job/recruitment/salary should map to 'placement'."""
        result = apply_synonyms("job salary package")
        assert "placement" in result
