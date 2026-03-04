"""
Centralized application configuration.

All paths, thresholds, and metadata are defined here so that
no module uses hardcoded magic values.
"""

import os
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = PROJECT_ROOT / "data"
FAQ_PATH = DATA_DIR / "faqs.json"
INTENTS_PATH = DATA_DIR / "intents.json"
MODEL_DIR = PROJECT_ROOT / "models"
INTENT_MODEL_PATH = MODEL_DIR / "intent_model.pkl"

# ── Confidence thresholds ─────────────────────────────────────────────────────
CONFIDENCE_HIGH = 0.5    # Score above this → 🟢 green
CONFIDENCE_MED = 0.3     # Score above this → 🟡 yellow, below → 🔴 red

# ── Context settings ─────────────────────────────────────────────────────────
CONTEXT_MAX_TURNS = 3    # Max conversation turns to keep in history

# ── App metadata ──────────────────────────────────────────────────────────────
APP_TITLE = "🎓 College FAQ Chatbot"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "An intelligent FAQ chatbot for college students — now with intent classification, entity extraction, and multi-turn context."

# ── Fallback responses ────────────────────────────────────────────────────────
FALLBACK_ANSWER = (
    "Sorry, I don't have an answer for that question yet. "
    "Please contact the college office for assistance."
)
EMPTY_QUERY_MSG = "Please ask a question about the college."
