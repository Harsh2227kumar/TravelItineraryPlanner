"""
Synonym expansion module.

Maps common student vocabulary variants to canonical keywords
so that queries like "tuition payment" match FAQs about "fees".

Introduced in: Week 3
"""

# ── Synonym Groups ────────────────────────────────────────────────────────────
# Each group maps variant words → a single canonical keyword.
# The canonical keyword is the FIRST item in each group.

SYNONYM_GROUPS = {
    "fees": [
        "fees", "fee", "tuition", "payment", "cost", "charges", "price",
        "pricing", "amount", "expense", "pay", "paying", "paid",
    ],
    "timetable": [
        "timetable", "schedule", "timing", "timings", "slots", "hours",
        "time", "clock", "when", "routine",
    ],
    "exam": [
        "exam", "exams", "test", "tests", "assessment", "evaluation",
        "examination", "paper", "papers", "midterm", "final",
    ],
    "contact": [
        "contact", "office", "reach", "helpdesk", "phone", "email",
        "call", "number", "address", "officer",
    ],
    "hostel": [
        "hostel", "accommodation", "dorm", "dormitory", "room",
        "boarding", "residence", "staying", "lodge", "mess",
    ],
    "scholarship": [
        "scholarship", "scholarships", "grant", "grants", "financial",
        "aid", "concession", "waiver", "merit", "stipend",
    ],
    "admission": [
        "admission", "admissions", "enroll", "enrollment", "apply",
        "application", "eligibility", "eligible", "joining", "seat",
    ],
    "placement": [
        "placement", "placements", "job", "jobs", "recruit", "recruitment",
        "hiring", "career", "package", "salary", "company", "companies",
    ],
}

# Build a reverse lookup: variant_word → canonical_keyword
_SYNONYM_MAP = {}
for canonical, variants in SYNONYM_GROUPS.items():
    for word in variants:
        _SYNONYM_MAP[word] = canonical


def apply_synonyms(text: str) -> str:
    """
    Replace synonym variants with their canonical keywords.

    Args:
        text: Preprocessed (lowercased, cleaned) query string.

    Returns:
        Query string with synonym variants replaced by canonical forms.
    """
    tokens = text.split()
    mapped = [_SYNONYM_MAP.get(token, token) for token in tokens]
    return " ".join(mapped)
