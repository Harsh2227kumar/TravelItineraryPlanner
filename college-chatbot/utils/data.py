"""Data loading helpers for standalone week scripts."""

import json
from pathlib import Path
from typing import Dict, List


def load_faqs() -> List[Dict[str, str]]:
    """Load FAQ records from data/faqs.json."""
    path = Path(__file__).resolve().parents[1] / "data" / "faqs.json"
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def load_intents() -> Dict:
    """Load intent definitions from data/intents.json."""
    path = Path(__file__).resolve().parents[1] / "data" / "intents.json"
    with open(path, encoding="utf-8") as file:
        return json.load(file)
