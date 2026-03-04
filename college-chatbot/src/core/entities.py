"""
Entity extraction module.

Extracts structured information from user queries:
- Dates (via spaCy NER)
- Course codes (via regex)
- Semester numbers (via regex)
"""

import re
from typing import Dict, List

import spacy

# Load spaCy model (lazy, cached)
_nlp = None


def _get_nlp():
    """Load the spaCy English model (cached after first call)."""
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise OSError(
                "spaCy model 'en_core_web_sm' not found. "
                "Install it with: python -m spacy download en_core_web_sm"
            )
    return _nlp


def extract_entities(query: str) -> Dict[str, List[str]]:
    """
    Extract structured entities from a raw query.

    Always returns a dict with consistent keys, even if values are empty.

    Args:
        query: Raw user question.

    Returns:
        Dict with keys: 'dates', 'course_codes', 'semester'.
    """
    nlp = _get_nlp()
    doc = nlp(query)

    entities = {
        "dates": [],
        "course_codes": [],
        "semester": [],
    }

    # Dates — spaCy NER
    entities["dates"] = [ent.text for ent in doc.ents if ent.label_ == "DATE"]

    # Course codes — custom regex (e.g., CS301, ME202)
    entities["course_codes"] = re.findall(r'\b[A-Z]{2,4}\s?\d{3}\b', query)

    # Semester numbers — custom regex (e.g., SEM 5, Semester 6)
    entities["semester"] = re.findall(
        r'\bSEM\s?\d\b|\b[Ss]emester\s?\d\b', query, re.IGNORECASE
    )

    return entities
