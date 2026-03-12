"""
Web channel adapter (Streamlit).

Wraps the channel-agnostic core_bot in a Streamlit web interface.
This is the proper web channel adapter that imports only from core_bot.py.

Usage:
    streamlit run channels/web_app.py

Introduced in: Week 9
"""

import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st  # noqa: E402

from core_bot import chat  # noqa: E402
from src.config import (  # noqa: E402
    APP_TITLE, APP_DESCRIPTION, APP_VERSION,
    HANDOVER_EMAIL, HANDOVER_PHONE, HANDOVER_HOURS,
    CONFIDENCE_HIGH, CONFIDENCE_MED,
)


# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(page_title="College FAQ Chatbot", page_icon="🎓", layout="centered")


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("ℹ️ About")
    st.write("**College FAQ Bot**")
    st.write(f"Version {APP_VERSION}")
    st.markdown("---")

    st.subheader("📚 Topics Covered")
    st.markdown(
        """
        - 💰 Fees & Payments
        - 🕐 Timings & Schedule
        - 📝 Exams & Results
        - 📞 Contacts & Office
        - 🏠 Hostel & Facilities
        - 🎓 Admissions & Courses
        - 🎯 Scholarships
        """
    )
    st.markdown("---")

    st.subheader("🎯 Supported Intents")
    intents = ["fees", "exams", "timetable", "hostel", "scholarships",
               "admissions", "contact", "placements", "campus", "academics"]
    for intent in intents:
        st.markdown(f"• `{intent}`")
    st.markdown("---")

    # Clear context button
    if st.button("🔄 Clear Context"):
        if "context" in st.session_state:
            st.session_state.context = {
                "last_intent": None,
                "last_entities": {"dates": [], "course_codes": [], "semester": []},
            }
        if "history" in st.session_state:
            st.session_state.history = []
        st.rerun()

    st.caption("Built with Streamlit • Python")


# ── Helper Functions ──────────────────────────────────────────────────────────
def confidence_color(score: float) -> str:
    """Return an emoji indicator based on the confidence score."""
    if score > CONFIDENCE_HIGH:
        return "🟢"
    elif score > CONFIDENCE_MED:
        return "🟡"
    else:
        return "🔴"


# ── Chat History ──────────────────────────────────────────────────────────────
if "web_history" not in st.session_state:
    st.session_state.web_history = []


# ── Main Area ─────────────────────────────────────────────────────────────────
st.title(APP_TITLE)
st.caption(APP_DESCRIPTION)

# Show chat history
if st.session_state.web_history:
    st.markdown("#### 💬 Chat History")
    for turn in st.session_state.web_history:
        st.markdown(f"**You:** {turn['user']}")
        st.markdown(f"**🤖 Bot:** {turn['bot']}")
        st.markdown("---")

# User input
user_input = st.text_input(
    "💬 Ask your question here...",
    placeholder="e.g. What are the college timings?",
    key="user_query",
)

if user_input:
    # Call the channel-agnostic core bot
    response = chat(user_input, channel="web")

    # Save to local history
    answer_text = response.get("answer", response.get("message", ""))
    st.session_state.web_history.append({"user": user_input, "bot": answer_text})
    if len(st.session_state.web_history) > 3:
        st.session_state.web_history = st.session_state.web_history[-3:]

    # ── Render based on response type ─────────────────────────────────────
    score = response.get("score", 0.0)

    if response["type"] == "answer":
        st.markdown("---")
        st.markdown("### 🤖 Answer")
        st.info(response["answer"])

        emoji = confidence_color(score)
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric(label="Confidence", value=f"{score:.2f}")
        with col2:
            st.markdown(f"### {emoji}")

    elif response["type"] == "fallback_soft":
        st.markdown("---")
        st.markdown("### 🤖 Answer")
        st.info(response.get("answer", ""))
        st.warning("⚠️ I'm not fully sure about that. Did you mean one of these?")
        for i, s in enumerate(response.get("suggestions", []), 1):
            with st.expander(f"{i}. {s['question']} (confidence: {s['score']:.2f})"):
                st.write(s["answer"])

    elif response["type"] == "fallback_hard":
        st.error("❌ I couldn't find a good answer for that question.")
        st.markdown("---")
        st.markdown("### 📞 Talk to a Human Advisor")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Email:** [{HANDOVER_EMAIL}](mailto:{HANDOVER_EMAIL})")
            st.markdown(f"**Phone:** {HANDOVER_PHONE}")
        with col2:
            st.markdown(f"**Office Hours:** {HANDOVER_HOURS}")

    # Show intent and entities for all types
    intent = response.get("intent")
    entities = response.get("entities", {})

    if intent:
        st.markdown(f"📌 **Intent detected:** `{intent}`")
    else:
        st.caption("📌 Intent: _not available (model not trained)_")

    has_entities = any(v for v in entities.values())
    if has_entities:
        with st.expander("🔍 Entities detected", expanded=False):
            if entities.get("dates"):
                st.markdown(f"• **Dates:** {', '.join(entities['dates'])}")
            if entities.get("course_codes"):
                st.markdown(f"• **Course Codes:** {', '.join(entities['course_codes'])}")
            if entities.get("semester"):
                st.markdown(f"• **Semester:** {', '.join(entities['semester'])}")
