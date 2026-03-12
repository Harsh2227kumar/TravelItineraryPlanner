"""
Channel-agnostic core bot.

This is the single entry point for ALL channels (web, CLI, WhatsApp).
No Streamlit imports here — this file is channel-independent.

Introduced in: Week 9
"""

from typing import Dict, Any

from src.core import get_answer, get_top_n_answers
from src.core.entities import extract_entities
from src.core.fallback import handle_response
from src.core.context import (
    resolve_context,
    update_context,
    add_to_history,
)


# ── Standalone context for non-Streamlit channels ─────────────────────────────
_cli_context = {
    "last_intent": None,
    "last_entities": {"dates": [], "course_codes": [], "semester": []},
}
_cli_history = []

_MAX_HISTORY = 3


def _update_cli_context(intent, entities):
    """Update context for CLI/WhatsApp channels (no session_state)."""
    _cli_context["last_intent"] = intent
    _cli_context["last_entities"] = entities


def _resolve_cli_context(intent, entities):
    """Resolve context from previous CLI turns."""
    resolved_intent = intent or _cli_context.get("last_intent") or "unknown"
    resolved_entities = dict(entities)
    last_ents = _cli_context.get("last_entities", {})
    for key in ("dates", "course_codes", "semester"):
        if not resolved_entities.get(key) and last_ents.get(key):
            resolved_entities[key] = last_ents[key]
    return resolved_intent, resolved_entities


def chat(user_input: str, channel: str = "web") -> Dict[str, Any]:
    """
    Process a user query and return a full response dict.

    This function is called by ALL channels identically.

    Args:
        user_input: Raw user question.
        channel: Channel identifier ('web', 'cli', 'whatsapp').

    Returns:
        Dict with keys: type, answer/message, score, intent, entities, channel.
    """
    # Get answer from the core pipeline
    answer, score, intent, entities = get_answer(user_input)

    # Apply fallback handling
    response = handle_response(
        query=user_input,
        answer=answer,
        score=score,
        get_top_n_fn=get_top_n_answers,
    )

    # Context handling — use Streamlit session state for web, standalone for CLI
    if channel == "web":
        try:
            intent, entities = resolve_context(user_input, intent, entities)
            update_context(intent, entities)
            add_to_history(user_input, answer)
        except Exception:
            pass  # Streamlit not available
    else:
        intent, entities = _resolve_cli_context(intent, entities)
        _update_cli_context(intent, entities)
        _cli_history.append({"user": user_input, "bot": answer})
        if len(_cli_history) > _MAX_HISTORY:
            _cli_history.pop(0)

    # Log interaction (Week 10)
    try:
        from src.core.analytics import log_interaction
        was_fallback = response["type"] != "answer"
        log_interaction(
            query=user_input,
            intent=intent or "unknown",
            confidence=score,
            answer=answer,
            was_fallback=was_fallback,
        )
    except ImportError:
        pass  # Analytics module not yet installed

    # Enrich response with metadata
    response["intent"] = intent
    response["entities"] = entities
    response["channel"] = channel

    return response
