"""
Core engine — public API.

This module is the single entry point for the bot's answering logic.
It orchestrates the full pipeline: preprocess → apply synonyms →
classify intent → extract entities → TF-IDF retrieve → return answer.
"""

from typing import Tuple, Dict, List, Optional

from src.data.loader import load_faqs
from src.core.matcher import KeywordMatcher
from src.core.retrieval import TFIDFRetriever
from src.core.preprocessor import preprocess
from src.core.synonyms import apply_synonyms
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
_tfidf_engine = None
_keyword_engine = None
_faqs = None


def _initialize():
    """Load data and create the active engines (called once on first query)."""
    global _tfidf_engine, _keyword_engine, _faqs
    _faqs = load_faqs()
    _tfidf_engine = TFIDFRetriever(_faqs)
    _keyword_engine = KeywordMatcher(_faqs)


def get_answer(query: str) -> Tuple[str, float, Optional[str], Dict[str, List[str]]]:
    """
    Answer a student query using the full pipeline.

    Pipeline:
        1. Preprocess the query (lowercase, remove stopwords/punctuation)
        2. Apply synonym expansion (map variants to canonical keywords)
        3. Predict intent (if model available)
        4. Extract entities (dates, course codes, semesters)
        5. Find best matching FAQ answer via TF-IDF (fallback to keyword)

    Args:
        query: Raw question string from the user.

    Returns:
        Tuple of (answer_text, confidence_score, intent, entities).
    """
    if _tfidf_engine is None:
        _initialize()

    # 1. Preprocess
    cleaned_query = preprocess(query)

    # 2. Apply synonym expansion
    expanded_query = apply_synonyms(cleaned_query)

    # 3. Predict intent (use original query for better accuracy)
    intent = None
    if _intent_available and INTENT_MODEL_PATH.exists():
        try:
            intent = predict_intent(query)
        except Exception:
            intent = None

    # 4. Extract entities (use original query to preserve casing for regex)
    entities = extract_entities(query)

    # 5. Find answer — TF-IDF primary, keyword fallback
    answer, score = _tfidf_engine.get_answer(query)

    # If TF-IDF confidence is very low, try keyword matcher as fallback
    if score < 0.1:
        kw_answer, kw_score = _keyword_engine.get_answer(expanded_query)
        if kw_score > score:
            answer, score = kw_answer, kw_score

    return answer, score, intent, entities


def get_top_n_answers(query: str, n: int = 3):
    """Return top N FAQ matches for a query (used by fallback system)."""
    if _tfidf_engine is None:
        _initialize()
    return _tfidf_engine.get_top_n(query, n)


def get_faqs():
    """Return the loaded FAQ list (initializes if needed)."""
    if _faqs is None:
        _initialize()
    return _faqs
