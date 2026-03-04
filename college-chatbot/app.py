"""
🎓 College FAQ Chatbot — Streamlit Entry Point.

This file is intentionally thin. All logic lives in src/.
Run with: streamlit run app.py
"""

import streamlit as st

from src.config import APP_TITLE, APP_DESCRIPTION
from src.core import get_answer
from src.ui.sidebar import render_sidebar
from src.ui.components import render_answer


# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(page_title="College FAQ Chatbot", page_icon="🎓", layout="centered")

# ── Sidebar ───────────────────────────────────────────────────────────────────
render_sidebar()

# ── Main Area ─────────────────────────────────────────────────────────────────
st.title(APP_TITLE)
st.caption(APP_DESCRIPTION)

user_input = st.text_input(
    "💬 Ask your question here...",
    placeholder="e.g. What are the college timings?",
)

if user_input:
    answer, score = get_answer(user_input)
    render_answer(answer, score)
