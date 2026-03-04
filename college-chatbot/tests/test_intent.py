"""
Unit tests for the intent classifier.

Run with: python -m pytest tests/test_intent.py -v
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import INTENTS_PATH  # noqa: E402


class TestIntentData:
    """Tests for the intents.json training data."""

    def test_intents_file_loads(self):
        """intents.json should load without errors."""
        with open(INTENTS_PATH, encoding="utf-8") as f:
            data = json.load(f)
        assert "intents" in data

    def test_minimum_7_intents(self):
        """Must have at least 7 intents defined (Rule R6)."""
        with open(INTENTS_PATH, encoding="utf-8") as f:
            data = json.load(f)
        assert len(data["intents"]) >= 7

    def test_minimum_15_examples_per_intent(self):
        """Each intent must have at least 15 examples (Rule R4)."""
        with open(INTENTS_PATH, encoding="utf-8") as f:
            data = json.load(f)
        for intent in data["intents"]:
            assert len(intent["examples"]) >= 15, (
                f"Intent '{intent['tag']}' has only {len(intent['examples'])} examples"
            )

    def test_required_fields(self):
        """Every intent must have 'tag', 'examples', and 'description' (Rule R15)."""
        with open(INTENTS_PATH, encoding="utf-8") as f:
            data = json.load(f)
        for intent in data["intents"]:
            assert "tag" in intent, f"Missing 'tag' in intent: {intent}"
            assert "examples" in intent, f"Missing 'examples' in intent: {intent}"
            assert "description" in intent, f"Missing 'description' in intent: {intent}"

    def test_no_duplicate_examples(self):
        """No duplicate examples across intents."""
        with open(INTENTS_PATH, encoding="utf-8") as f:
            data = json.load(f)
        all_examples = []
        for intent in data["intents"]:
            all_examples.extend(intent["examples"])
        assert len(all_examples) == len(set(all_examples)), "Duplicate examples found"
