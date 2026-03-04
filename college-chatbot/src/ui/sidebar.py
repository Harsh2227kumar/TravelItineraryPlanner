"""
Sidebar layout for the Streamlit app.

Separated into its own module so multiple developers can
edit sidebar content without touching the main app.py.
"""

import streamlit as st

from src.config import APP_VERSION


def render_sidebar():
    """Render the sidebar with app info and topic list."""
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
            """
        )
        st.markdown("---")
        st.caption("Built with Streamlit • Python")
