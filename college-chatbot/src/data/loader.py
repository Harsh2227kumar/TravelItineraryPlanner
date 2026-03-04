"""
FAQ data loader.

Loads and validates the FAQ JSON file. This is the single source
of truth for data access — no other module reads faqs.json directly.
"""

import json
from typing import List, Dict

from src.config import FAQ_PATH


def load_faqs(filepath=None) -> List[Dict[str, str]]:
    """
    Load FAQ entries from the JSON file.

    Args:
        filepath: Optional override path. Defaults to config.FAQ_PATH.

    Returns:
        List of dicts, each with at least 'question' and 'answer' keys.

    Raises:
        FileNotFoundError: If the FAQ file does not exist.
        ValueError: If any entry is missing required fields.
    """
    path = filepath or FAQ_PATH

    with open(path, encoding="utf-8") as f:
        faqs = json.load(f)

    # Validate entries
    for i, entry in enumerate(faqs):
        if "question" not in entry or "answer" not in entry:
            raise ValueError(
                f"FAQ entry {i} is missing required fields 'question' and/or 'answer'."
            )

    return faqs


def get_categories(faqs: List[Dict[str, str]]) -> List[str]:
    """Return a sorted list of unique categories found in the FAQ data."""
    categories = {faq.get("category", "general") for faq in faqs}
    return sorted(categories)
