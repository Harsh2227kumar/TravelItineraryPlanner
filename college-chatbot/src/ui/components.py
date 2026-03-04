"""
Reusable Streamlit UI components.

All answer rendering, badges, and display helpers live here
so that app.py stays clean and focused on layout only.
"""

import streamlit as st

from src.config import CONFIDENCE_HIGH, CONFIDENCE_MED


def confidence_color(score: float) -> str:
    """Return an emoji indicator based on the confidence score."""
    if score > CONFIDENCE_HIGH:
        return "🟢"
    elif score > CONFIDENCE_MED:
        return "🟡"
    else:
        return "🔴"


def render_answer(answer: str, score: float):
    """
    Display the bot's answer along with a color-coded confidence badge.

    Args:
        answer: The answer text to display.
        score: Confidence score between 0 and 1.
    """
    st.markdown("---")
    st.markdown("### 🤖 Answer")
    st.info(answer)

    # Confidence badge
    emoji = confidence_color(score)
    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric(label="Confidence", value=f"{score:.2f}")
    with col2:
        st.markdown(f"### {emoji}")
        if score < CONFIDENCE_MED:
            st.warning(
                "Low confidence — the answer may not be relevant. "
                "Try rephrasing your question."
            )
