"""Synonym mapping utility for weekly scripts."""

SYNONYM_GROUPS = {
    "fees": ["fees", "fee", "tuition", "payment", "cost", "charges"],
    "timetable": ["timetable", "schedule", "timing", "timings", "slots"],
    "exam": ["exam", "exams", "test", "assessment", "evaluation"],
    "contact": ["contact", "office", "reach", "helpdesk", "phone", "email"],
}

_SYNONYM_MAP = {
    word: canonical
    for canonical, variants in SYNONYM_GROUPS.items()
    for word in variants
}


def apply_synonyms(text: str) -> str:
    """Replace known synonyms with canonical forms."""
    return " ".join(_SYNONYM_MAP.get(token, token) for token in text.split())
