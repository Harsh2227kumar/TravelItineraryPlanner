"""
Fallback and handover handler.

Provides intelligent fallback responses when the bot cannot
confidently answer a query. Implements two-level fallback:
  - Soft fallback: suggest similar FAQs + ask for clarification
  - Hard fallback: route to human advisor with contact info

Introduced in: Week 8
"""

from typing import Dict, Any, List

from src.config import (
    FALLBACK_SOFT_THRESHOLD,
    FALLBACK_HARD_THRESHOLD,
    TOP_N_SUGGESTIONS,
    HANDOVER_EMAIL,
    HANDOVER_PHONE,
    HANDOVER_HOURS,
    FALLBACK_ANSWER,
)


def handle_response(query: str, answer: str, score: float,
                     get_top_n_fn=None) -> Dict[str, Any]:
    """
    Wrap a bot response with fallback handling.

    Args:
        query: Original user question.
        answer: Bot's best answer.
        score: Confidence score (0–1).
        get_top_n_fn: Callable to get top N FAQ matches (injected from core).

    Returns:
        Response dict with type ('answer', 'fallback_soft', or 'fallback_hard').
    """
    # ✅ Confident answer
    if score > FALLBACK_SOFT_THRESHOLD:
        return {
            "type": "answer",
            "answer": answer,
            "score": score,
        }

    # ⚠️ Soft fallback — suggest similar FAQs
    if score >= FALLBACK_HARD_THRESHOLD:
        suggestions = []
        if get_top_n_fn:
            top_matches = get_top_n_fn(query, TOP_N_SUGGESTIONS)
            suggestions = [
                {"question": q, "answer": a, "score": s}
                for q, a, s in top_matches
            ]

        return {
            "type": "fallback_soft",
            "answer": answer,
            "score": score,
            "clarification": "I'm not fully sure about that. Did you mean one of these?",
            "suggestions": suggestions,
        }

    # ❌ Hard fallback — route to human
    return {
        "type": "fallback_hard",
        "message": FALLBACK_ANSWER,
        "score": score,
        "advisor": {
            "email": HANDOVER_EMAIL,
            "phone": HANDOVER_PHONE,
            "hours": HANDOVER_HOURS,
            "mailto_link": f"mailto:{HANDOVER_EMAIL}?subject=Student Query: {query[:50]}",
        },
    }


def format_suggestions_text(suggestions: List[Dict]) -> str:
    """Format FAQ suggestions as numbered text (for CLI/WhatsApp channels)."""
    if not suggestions:
        return ""
    lines = ["Did you mean one of these?\n"]
    for i, s in enumerate(suggestions, 1):
        lines.append(f"  {i}. {s['question']}")
    return "\n".join(lines)


def format_handover_text() -> str:
    """Format handover contact info as text (for CLI/WhatsApp channels)."""
    return (
        f"📞 Contact the college office for help:\n"
        f"   Email: {HANDOVER_EMAIL}\n"
        f"   Phone: {HANDOVER_PHONE}\n"
        f"   Hours: {HANDOVER_HOURS}"
    )
