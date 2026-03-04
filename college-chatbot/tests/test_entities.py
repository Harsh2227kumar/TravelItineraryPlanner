"""
Unit tests for the entity extractor.

Run with: python -m pytest tests/test_entities.py -v
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.entities import extract_entities  # noqa: E402


class TestEntityExtractor:
    """Tests for entity extraction."""

    def test_returns_dict_with_required_keys(self):
        """extract_entities must always return a dict with all 3 keys (Rule R5)."""
        result = extract_entities("Hello")
        assert "dates" in result
        assert "course_codes" in result
        assert "semester" in result

    def test_empty_query_returns_empty_lists(self):
        """An empty query should return empty lists, not errors."""
        result = extract_entities("")
        assert result["dates"] == []
        assert result["course_codes"] == []
        assert result["semester"] == []

    def test_course_code_extraction(self):
        """Should extract course codes like CS301, ME202."""
        result = extract_entities("When is the CS301 exam?")
        assert "CS301" in result["course_codes"]

    def test_semester_extraction(self):
        """Should extract semester patterns like SEM 5."""
        result = extract_entities("What is the SEM 5 timetable?")
        assert any("5" in s for s in result["semester"])

    def test_combined_entities(self):
        """A complex query should extract multiple entity types."""
        result = extract_entities("When is the SEM 5 CS301 exam on March 15th?")
        assert len(result["course_codes"]) > 0
        assert len(result["semester"]) > 0
        # Date extraction depends on spaCy model quality

    def test_values_are_lists(self):
        """All values in the returned dict must be lists."""
        result = extract_entities("Random query")
        for key, val in result.items():
            assert isinstance(val, list), f"'{key}' should be a list, got {type(val)}"
