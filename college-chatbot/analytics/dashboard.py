"""
📊 Chatbot Analytics Dashboard.

Reads interaction logs from the SQLite database and displays
charts and metrics for monitoring chatbot performance.

Run with: streamlit run analytics/dashboard.py
Introduced in: Week 10
"""

import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import streamlit as st  # noqa: E402
import pandas as pd  # noqa: E402

from src.core.analytics import (  # noqa: E402
    get_logs_df,
    get_analytics_summary,
    suggest_improvements,
)


# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Chatbot Analytics", page_icon="📊", layout="wide")
st.title("📊 Chatbot Analytics Dashboard")
st.caption("Monitor chatbot performance, track intents, and identify improvements.")

# ── Load Data via FastAPI ───────────────────────────────────────────────────
API_URL = os.getenv("API_URL", "http://localhost:8000")

@st.cache_data(ttl=10) # Cache for 10 seconds to avoid spamming the backend
def fetch_analytics_data():
    try:
        summary_res = requests.get(f"{API_URL}/analytics/summary", timeout=5)
        summary_res.raise_for_status()
        summary = summary_res.json()

        logs_res = requests.get(f"{API_URL}/analytics/logs", timeout=5)
        logs_res.raise_for_status()
        df = pd.DataFrame(logs_res.json())
        
        return summary, df
    except Exception as e:
        st.error(f"Cannot connect to FastAPI backend: {e}")
        return None, pd.DataFrame()

summary, df = fetch_analytics_data()

if summary is None:
    st.stop()

if df.empty:
    st.warning("No interactions logged yet. Start chatting with the bot to generate data!")
    st.stop()

# ── Metric Cards ─────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Queries", summary["total_queries"])
with col2:
    st.metric("Avg Confidence", f"{summary['avg_confidence']:.2f}")
with col3:
    st.metric("Fallback Rate", f"{summary['fallback_rate']:.1f}%")
with col4:
    top_intent = max(summary["top_intents"], key=summary["top_intents"].get) if summary["top_intents"] else "—"
    st.metric("Top Intent", top_intent)

st.markdown("---")

# ── Charts ───────────────────────────────────────────────────────────────────
left, right = st.columns(2)

with left:
    st.subheader("📈 Queries Over Time")
    if "timestamp" in df.columns:
        df["date"] = pd.to_datetime(df["timestamp"]).dt.date
        daily = df.groupby("date").size().reset_index(name="count")
        st.line_chart(daily.set_index("date"))

with right:
    st.subheader("🎯 Intent Distribution")
    if summary["top_intents"]:
        intent_df = pd.DataFrame(
            list(summary["top_intents"].items()),
            columns=["Intent", "Count"],
        )
        st.bar_chart(intent_df.set_index("Intent"))

st.markdown("---")

# ── Confidence Distribution ──────────────────────────────────────────────────
st.subheader("📊 Confidence Score Distribution")
st.bar_chart(pd.cut(df["confidence"], bins=10).value_counts().sort_index())

st.markdown("---")

# ── Top Unhandled Queries ────────────────────────────────────────────────────
st.subheader("📋 Top Unhandled Queries (Low Confidence)")
low_conf = summary.get("low_confidence_queries", [])
if low_conf:
    st.dataframe(pd.DataFrame(low_conf), use_container_width=True)
else:
    st.success("No low-confidence queries — the bot is handling everything well!")

st.markdown("---")

# ── Improvement Suggestions ──────────────────────────────────────────────────
st.subheader("💡 Improvement Proposals")
# Generate basic improvements based on the data we fetched
if not df.empty:
    weak_intents = df.groupby("intent")["confidence"].mean().sort_values().head(2)
    st.markdown("**Intents that need more training examples:**")
    for intent, conf in weak_intents.items():
        st.markdown(f"- `{intent}` (Average Confidence: {conf:.2f})")
else:
    st.markdown("- Need more data to generate suggestions.")

# ── Raw Logs ─────────────────────────────────────────────────────────────────
with st.expander("🗃️ Raw Interaction Logs"):
    st.dataframe(df.head(100), use_container_width=True)
