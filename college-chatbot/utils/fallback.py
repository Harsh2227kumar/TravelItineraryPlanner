"""Fallback utility for weekly scripts."""

from typing import Any, Dict, List


def handle_response(query: str, answer: str, score: float, top_matches: List = None) -> Dict[str, Any]:
    """Return answer, soft fallback, or hard fallback payload."""
    if score > 0.3:
        return {"type": "answer", "answer": answer, "score": score}

    if score >= 0.2:
        suggestions = []
        if top_matches:
            suggestions = [
                {"question": item[0], "answer": item[1], "score": item[2]}
                for item in top_matches
            ]
        return {
            "type": "fallback_soft",
            "answer": answer,
            "score": score,
            "clarification": "I'm not fully sure about that. Did you mean one of these?",
            "suggestions": suggestions,
        }

    return {
        "type": "fallback_hard",
        "score": score,
        "message": "I don't have a confident answer. Please contact the admission office.",
    }
