"""
🎓 College FAQ Chatbot — Streamlit Entry Point.

This file is intentionally thin. All logic lives in src/.
Run with: streamlit run app.py
"""

import streamlit as st

from src.config import APP_TITLE, APP_DESCRIPTION
from src.core import get_answer
from src.core.context import (
    resolve_context,
    update_context,
    add_to_history,
    get_history,
)
from src.ui.sidebar import render_sidebar
from src.ui.components import (
    render_answer,
    render_intent_badge,
    render_entities,
    render_chat_history,
)


# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(page_title="College FAQ Chatbot", page_icon="🎓", layout="centered")

# ── Sidebar ───────────────────────────────────────────────────────────────────
render_sidebar()

# ── Main Area ─────────────────────────────────────────────────────────────────
st.title(APP_TITLE)
st.caption(APP_DESCRIPTION)

# Show chat history above the input
history = get_history()
render_chat_history(history)

# User input
user_input = st.text_input(
    "💬 Ask your question here...",
    placeholder="e.g. What are the college timings?",
    key="user_query",
)

if user_input:
    # Run the full pipeline
    answer, score, intent, entities = get_answer(user_input)

    # Resolve context for follow-up queries
    intent, entities = resolve_context(user_input, intent, entities)

    # Update context with current turn
    update_context(intent, entities)

    # Add to history
    add_to_history(user_input, answer)

    # Render results
    render_answer(answer, score)
    render_intent_badge(intent)
    render_entities(entities)
