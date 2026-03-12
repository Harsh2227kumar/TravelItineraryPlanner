"""
Reusable Streamlit UI components.

All answer rendering, badges, and display helpers live here
so that app.py stays clean and focused on layout only.
"""

from typing import Dict, List, Optional
import streamlit as st

from src.config import (
    CONFIDENCE_HIGH, 
    CONFIDENCE_MED,
    HANDOVER_EMAIL,
    HANDOVER_PHONE,
    HANDOVER_HOURS
)


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


def render_intent_badge(intent: Optional[str]):
    """
    Display the detected intent as a styled badge.

    Args:
        intent: Detected intent tag, or None if unavailable.
    """
    if intent:
        st.markdown(f"📌 **Intent detected:** `{intent}`")
    else:
        st.caption("📌 Intent: _not available (model not trained)_")


def render_entities(entities: Dict[str, List[str]]):
    """
    Display extracted entities in a collapsible expander.

    Args:
        entities: Dict with keys 'dates', 'course_codes', 'semester'.
    """
    has_entities = any(v for v in entities.values())
    if has_entities:
        with st.expander("🔍 Entities detected", expanded=False):
            if entities.get("dates"):
                st.markdown(f"• **Dates:** {', '.join(entities['dates'])}")
            if entities.get("course_codes"):
                st.markdown(f"• **Course Codes:** {', '.join(entities['course_codes'])}")
            if entities.get("semester"):
                st.markdown(f"• **Semester:** {', '.join(entities['semester'])}")


def render_chat_history(history: List[Dict[str, str]]):
    """
    Display the conversation history in a chat-style format.

    Args:
        history: List of dicts with 'user' and 'bot' keys.
    """
    if not history:
        return

    st.markdown("#### 💬 Chat History")
    for turn in history:
        st.markdown(f"**You:** {turn['user']}")
        st.markdown(f"**🤖 Bot:** {turn['bot']}")
        st.markdown("---")

def render_fallback_ui(message: str, suggestions: List[Dict[str, str]] = None, show_advisor: bool = False):
    """
    Display a fallback UI with optional suggestions and advisor contact info.
    """
    st.markdown("---")
    st.warning(message)
    
    if suggestions:
        st.markdown("**Did you mean one of these?**")
        for i, s in enumerate(suggestions, 1):
            score = s.get('score', 0)
            with st.expander(f"{i}. {s['question']} (confidence: {score:.2f})"):
                st.write(s['answer'])
                
    if show_advisor:
        st.markdown("---")
        st.markdown("### 📞 Talk to a Human Advisor")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Email:** [{HANDOVER_EMAIL}](mailto:{HANDOVER_EMAIL})")
            st.markdown(f"**Phone:** {HANDOVER_PHONE}")
        with col2:
            st.markdown(f"**Office Hours:** {HANDOVER_HOURS}")

