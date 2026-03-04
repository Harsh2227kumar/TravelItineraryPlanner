"""
Core engine — public API.

This module is the single entry point for the bot's answering logic.
It initializes the active engine and exposes `get_answer()`.

When new engines are added (TF-IDF, intent classifier, etc.), they
plug in here — no changes needed in app.py or UI code.
"""

from typing import Tuple

from src.data.loader import load_faqs
from src.core.matcher import KeywordMatcher

# ── Module-level state (lazy-initialized) ─────────────────────────────────────
_engine = None
_faqs = None


def _initialize():
    """Load data and create the active engine (called once on first query)."""
    global _engine, _faqs
    _faqs = load_faqs()
    _engine = KeywordMatcher(_faqs)


def get_answer(query: str) -> Tuple[str, float]:
    """
    Answer a student query using the currently active engine.

    Args:
        query: Raw question string from the user.

    Returns:
        Tuple of (answer_text, confidence_score).
    """
    if _engine is None:
        _initialize()
    return _engine.get_answer(query)


def get_faqs():
    """Return the loaded FAQ list (initializes if needed)."""
    if _faqs is None:
        _initialize()
    return _faqs
