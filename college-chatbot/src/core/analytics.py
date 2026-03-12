"""
Interaction logger and analytics engine.

Logs every chatbot interaction to a SQLite database
and provides analytics functions for dashboarding.

Introduced in: Week 10
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd

from src.config import PROJECT_ROOT

# ── Database path ─────────────────────────────────────────────────────────────
DB_DIR = PROJECT_ROOT / "data" / "logs"
DB_PATH = DB_DIR / "interactions.db"


def init_db():
    """Create the interactions database and table if they don't exist."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp    TEXT    NOT NULL,
            query        TEXT    NOT NULL,
            intent       TEXT,
            confidence   REAL,
            answer       TEXT,
            was_fallback INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def log_interaction(query: str, intent: str, confidence: float,
                     answer: str, was_fallback: bool = False):
    """
    Write a single interaction row to the database.

    Args:
        query: The user's question.
        intent: Predicted intent tag.
        confidence: Confidence score (0–1).
        answer: Bot's response text.
        was_fallback: Whether a fallback was triggered.
    """
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """INSERT INTO logs (timestamp, query, intent, confidence, answer, was_fallback)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            datetime.now().isoformat(),
            query,
            intent,
            confidence,
            answer,
            1 if was_fallback else 0,
        ),
    )
    conn.commit()
    conn.close()


def get_logs_df() -> pd.DataFrame:
    """
    Read all logged interactions as a pandas DataFrame.

    Returns:
        DataFrame with columns: id, timestamp, query, intent, confidence, answer, was_fallback.
    """
    init_db()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM logs ORDER BY id DESC", conn)
    conn.close()
    return df


def get_analytics_summary() -> dict:
    """
    Compute analytics summary from logged interactions.

    Returns:
        Dict with total_queries, avg_confidence, fallback_rate,
        top_intents, and low_confidence_queries.
    """
    df = get_logs_df()

    if df.empty:
        return {
            "total_queries": 0,
            "avg_confidence": 0.0,
            "fallback_rate": 0.0,
            "top_intents": [],
            "low_confidence_queries": [],
        }

    total = len(df)
    avg_conf = df["confidence"].mean()
    fallback_rate = df["was_fallback"].mean() * 100

    # Top intents
    top_intents = (
        df["intent"]
        .value_counts()
        .head(10)
        .to_dict()
    )

    # Low confidence queries (for improvement)
    low_conf = (
        df[df["confidence"] < 0.3]
        .nlargest(10, "id")[["query", "intent", "confidence"]]
        .to_dict("records")
    )

    return {
        "total_queries": total,
        "avg_confidence": round(avg_conf, 3),
        "fallback_rate": round(fallback_rate, 1),
        "top_intents": top_intents,
        "low_confidence_queries": low_conf,
    }


def suggest_improvements() -> list:
    """
    Suggest improvements based on observed query patterns.

    Returns:
        List of improvement suggestion strings.
    """
    df = get_logs_df()
    suggestions = []

    if df.empty:
        return ["No interactions logged yet. Start chatting to generate data!"]

    # High fallback rate
    fallback_rate = df["was_fallback"].mean() * 100
    if fallback_rate > 20:
        suggestions.append(
            f"⚠️ Fallback rate is {fallback_rate:.1f}% — consider adding more FAQs "
            f"or training examples for weak intents."
        )

    # Intents with low average confidence
    intent_conf = df.groupby("intent")["confidence"].mean()
    weak_intents = intent_conf[intent_conf < 0.4]
    for intent, conf in weak_intents.items():
        suggestions.append(
            f"📉 Intent '{intent}' has low avg confidence ({conf:.2f}) — "
            f"add more training examples."
        )

    # Frequently asked but poorly answered
    low_conf_queries = df[df["confidence"] < 0.2]["query"].value_counts().head(5)
    for query, count in low_conf_queries.items():
        if count >= 2:
            suggestions.append(
                f"🔄 Query \"{query}\" was asked {count} times with low confidence — "
                f"consider adding a FAQ for this."
            )

    if not suggestions:
        suggestions.append("✅ The chatbot is performing well! No immediate improvements needed.")

    return suggestions
