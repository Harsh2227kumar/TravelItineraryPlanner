"""Entity extraction utility for weekly scripts."""

import re
from typing import Dict, List

import spacy

_NLP = None


def _get_nlp():
    """Load spaCy model lazily."""
    global _NLP
    if _NLP is None:
        _NLP = spacy.load("en_core_web_sm")
    return _NLP


def extract_entities(query: str) -> Dict[str, List[str]]:
    """Extract dates, course codes, and semester markers."""
    doc = _get_nlp()(query)
    return {
        "dates": [ent.text for ent in doc.ents if ent.label_ == "DATE"],
        "course_codes": re.findall(r"\b[A-Z]{2,4}\s?\d{3}\b", query),
        "semester": re.findall(r"\bSEM\s?\d\b|\b[Ss]emester\s?\d\b", query, re.IGNORECASE),
    }
