"""
Core engine — public API.

This module is the single entry point for the bot's answering logic.
It orchestrates the full pipeline: preprocess → classify intent →
extract entities → keyword match → return answer.
"""

from typing import Tuple, Dict, List, Optional

from src.data.loader import load_faqs
from src.core.matcher import KeywordMatcher
from src.core.preprocessor import preprocess
from src.core.entities import extract_entities

# Intent module is optional — only used if the model is trained
_intent_available = False
try:
    from src.core.intent import predict_intent
    from src.config import INTENT_MODEL_PATH
    _intent_available = True
except ImportError:
    pass

# ── Module-level state (lazy-initialized) ─────────────────────────────────────
_engine = None
_faqs = None


def _initialize():
    """Load data and create the active engine (called once on first query)."""
    global _engine, _faqs
    _faqs = load_faqs()
    _engine = KeywordMatcher(_faqs)


def get_answer(query: str) -> Tuple[str, float, Optional[str], Dict[str, List[str]]]:
    """
    Answer a student query using the full pipeline.

    Pipeline:
        1. Preprocess the query (lowercase, remove stopwords/punctuation)
        2. Predict intent (if model available)
        3. Extract entities (dates, course codes, semesters)
        4. Find best matching FAQ answer

    Args:
        query: Raw question string from the user.

    Returns:
        Tuple of (answer_text, confidence_score, intent, entities).
    """
    if _engine is None:
        _initialize()

    # 1. Preprocess
    cleaned_query = preprocess(query)

    # 2. Predict intent (use original query for better accuracy)
    intent = None
    if _intent_available and INTENT_MODEL_PATH.exists():
        try:
            intent = predict_intent(query)
        except Exception:
            intent = None

    # 3. Extract entities (use original query to preserve casing for regex)
    entities = extract_entities(query)

    # 4. Find answer using preprocessed query for matching
    answer, score = _engine.get_answer(cleaned_query)

    return answer, score, intent, entities


def get_faqs():
    """Return the loaded FAQ list (initializes if needed)."""
    if _faqs is None:
        _initialize()
    return _faqs
