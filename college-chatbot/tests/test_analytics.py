"""
Unit tests for the analytics module.

Run with: python -m pytest tests/test_analytics.py -v
"""

import sys
import os
import sqlite3
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.analytics import (  # noqa: E402
    init_db,
    log_interaction,
    get_logs_df,
    get_analytics_summary,
    suggest_improvements,
    DB_PATH,
)


class TestAnalytics:
    """Test suite for the analytics engine (uses temp DB)."""

    def test_init_db_creates_table(self):
        """init_db should create the logs table."""
        init_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='logs'"
        )
        tables = cursor.fetchall()
        conn.close()
        assert len(tables) == 1

    def test_log_interaction_writes_row(self):
        """log_interaction should write a row to the database."""
        init_db()
        log_interaction("test query", "exams", 0.85, "Test answer", False)
        df = get_logs_df()
        assert len(df) > 0
        assert df.iloc[0]["query"] == "test query"

    def test_get_logs_df_returns_dataframe(self):
        """get_logs_df should return a pandas DataFrame."""
        init_db()
        df = get_logs_df()
        assert hasattr(df, "columns")
        assert "query" in df.columns

    def test_get_analytics_summary_structure(self):
        """Summary should have required keys."""
        summary = get_analytics_summary()
        assert "total_queries" in summary
        assert "avg_confidence" in summary
        assert "fallback_rate" in summary
        assert "top_intents" in summary

    def test_suggest_improvements_returns_list(self):
        """suggest_improvements should return a list of strings."""
        suggestions = suggest_improvements()
        assert isinstance(suggestions, list)
        assert all(isinstance(s, str) for s in suggestions)
