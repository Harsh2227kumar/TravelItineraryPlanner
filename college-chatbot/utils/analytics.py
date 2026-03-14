"""Analytics utility for weekly scripts."""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "logs" / "interactions_weeks.db"


def init_db():
    """Initialize week-track analytics database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            query TEXT NOT NULL,
            intent TEXT,
            confidence REAL,
            answer TEXT,
            was_fallback INTEGER DEFAULT 0
        )
        """
    )
    connection.commit()
    connection.close()


def log_interaction(query: str, intent: str, confidence: float, answer: str, was_fallback: bool):
    """Insert one interaction row."""
    init_db()
    connection = sqlite3.connect(DB_PATH)
    connection.execute(
        "INSERT INTO logs (timestamp, query, intent, confidence, answer, was_fallback) VALUES (?, ?, ?, ?, ?, ?)",
        (datetime.now().isoformat(), query, intent, confidence, answer, 1 if was_fallback else 0),
    )
    connection.commit()
    connection.close()


def get_summary() -> Dict:
    """Return summary metrics for week-10 report."""
    init_db()
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM logs")
    total_queries = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(AVG(confidence), 0) FROM logs")
    avg_confidence = float(cursor.fetchone()[0] or 0)

    cursor.execute("SELECT COALESCE(AVG(was_fallback), 0) FROM logs")
    fallback_rate = float(cursor.fetchone()[0] or 0) * 100

    cursor.execute("SELECT intent, COUNT(*) AS c FROM logs GROUP BY intent ORDER BY c DESC LIMIT 5")
    top_intents = {row[0]: row[1] for row in cursor.fetchall() if row[0]}

    connection.close()
    return {
        "total_queries": total_queries,
        "avg_confidence": round(avg_confidence, 3),
        "fallback_rate": round(fallback_rate, 1),
        "top_intents": top_intents,
    }


def suggest_improvements() -> List[str]:
    """Return simple improvement recommendations."""
    summary = get_summary()
    suggestions: List[str] = []

    if summary["total_queries"] == 0:
        return ["No interactions logged yet. Run week9/week10 demos first."]

    if summary["fallback_rate"] > 20:
        suggestions.append("Add more FAQ entries for low-confidence queries.")
    if summary["avg_confidence"] < 0.6:
        suggestions.append("Improve intent examples and retrain classifier.")
    if not suggestions:
        suggestions.append("System is stable. Continue monitoring weekly trends.")
    return suggestions
