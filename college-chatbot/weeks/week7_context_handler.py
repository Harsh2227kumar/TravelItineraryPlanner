"""Week 7: Context handling demo (non-Streamlit fallback context)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core_bot import chat


def run_demo():
    """Run a multi-turn demo through the channel-agnostic bot."""
    print("Week 7 - Context Handling for Follow-ups")
    conversation = [
        "When are the semester exams?",
        "What about SEM 5?",
        "And CS301?",
    ]

    for query in conversation:
        response = chat(query, channel="cli")
        text = response.get("answer") or response.get("message", "")
        print(f"You: {query}")
        print(f"Bot: {text}")
        print(f"Intent: {response.get('intent')}")
        print(f"Entities: {response.get('entities')}\n")


if __name__ == "__main__":
    run_demo()
