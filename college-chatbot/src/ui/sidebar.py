"""
Sidebar layout for the Streamlit app.

Separated into its own module so multiple developers can
edit sidebar content without touching the main app.py.
"""

import streamlit as st

from src.config import APP_VERSION


def render_sidebar():
    """Render the sidebar with app info, intent list, and controls."""
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
        intents = ["fees", "exams", "timetable", "hostel", "scholarships", "admissions", "contact", "placements", "campus", "academics"]
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
