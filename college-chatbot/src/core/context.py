"""
Context manager for multi-turn conversations.

Tracks the last intent, entities, and conversation history using
Streamlit's session_state. Handles follow-up resolution when
the current query is vague.
"""

from typing import Dict, List, Optional, Tuple
import streamlit as st

from src.config import CONTEXT_MAX_TURNS


def _ensure_context():
    """Initialize context in session state if not present."""
    if "context" not in st.session_state:
        st.session_state.context = {
            "last_intent": None,
            "last_entities": {"dates": [], "course_codes": [], "semester": []},
        }
    if "history" not in st.session_state:
        st.session_state.history = []


def update_context(intent: str, entities: Dict[str, List[str]]):
    """
    Save the current intent and entities into session state.

    Args:
        intent: Detected intent tag.
        entities: Extracted entities dict.
    """
    _ensure_context()
    st.session_state.context["last_intent"] = intent
    st.session_state.context["last_entities"] = entities


def resolve_context(
    query: str, intent: Optional[str], entities: Dict[str, List[str]]
) -> Tuple[str, Dict[str, List[str]]]:
    """
    Enrich the current intent and entities using previous conversation context.

    If the current query lacks an intent or entities, fill them in from the
    last turn's context.

    Args:
        query: Current raw query.
        intent: Currently detected intent (may be None or vague).
        entities: Currently extracted entities.

    Returns:
        Tuple of (resolved_intent, resolved_entities).
    """
    _ensure_context()
    ctx = st.session_state.context

    # If no clear intent detected, use previous
    resolved_intent = intent
    if not resolved_intent:
        resolved_intent = ctx.get("last_intent") or "unknown"

    # Fill in missing entity types from previous context
    resolved_entities = dict(entities)
    last_ents = ctx.get("last_entities", {})
    for key in ("dates", "course_codes", "semester"):
        if not resolved_entities.get(key) and last_ents.get(key):
            resolved_entities[key] = last_ents[key]

    return resolved_intent, resolved_entities


def add_to_history(user_msg: str, bot_msg: str):
    """
    Append a conversation turn to history, capped at CONTEXT_MAX_TURNS.

    Args:
        user_msg: The user's question.
        bot_msg: The bot's response.
    """
    _ensure_context()
    st.session_state.history.append({"user": user_msg, "bot": bot_msg})
    # Keep only last N turns
    if len(st.session_state.history) > CONTEXT_MAX_TURNS:
        st.session_state.history = st.session_state.history[-CONTEXT_MAX_TURNS:]


def get_history() -> List[Dict[str, str]]:
    """Return the conversation history (last N turns)."""
    _ensure_context()
    return st.session_state.history


def clear_context():
    """Reset context and history."""
    st.session_state.context = {
        "last_intent": None,
        "last_entities": {"dates": [], "course_codes": [], "semester": []},
    }
    st.session_state.history = []
