"""Week 9: Multichannel logic mock demo via channel-agnostic core bot."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core_bot import chat


def run_demo():
    """Demonstrate same bot response shape across channels."""
    print("Week 9 - Multichannel Deployment Mockup\n")
    query = "What is the hostel fee?"

    for channel in ["web", "cli", "whatsapp"]:
        response = chat(query, channel=channel)
        text = response.get("answer") or response.get("message", "")
        print(f"Channel: {channel}")
        print(f"Bot: {text}")
        print(f"Type: {response.get('type')} | Intent: {response.get('intent')}\n")


if __name__ == "__main__":
    run_demo()
