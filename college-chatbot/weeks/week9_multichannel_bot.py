"""Week 9: Multichannel logic mock demo via channel-agnostic core bot."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data import load_faqs
from utils.entities import extract_entities
from utils.fallback import handle_response
from utils.intent import predict_intent, train_classifier
from utils.retrieval import TfidfFaqBot


def chat(query: str, channel: str, bot: TfidfFaqBot) -> dict:
    """Run shared logic for a mock channel and return response payload."""
    intent = predict_intent(query)
    entities = extract_entities(query)
    answer, score = bot.get_answer(query)
    response = handle_response(query, answer, score, bot.get_top_n(query, 3))
    response["intent"] = intent
    response["entities"] = entities
    response["channel"] = channel
    return response


def run_demo():
    """Demonstrate same bot response shape across channels."""
    print("Week 9 - Multichannel Deployment Mockup\n")
    faqs = load_faqs()
    bot = TfidfFaqBot(faqs)
    train_classifier()

    query = "What is the hostel fee?"

    for channel in ["web", "cli", "whatsapp"]:
        response = chat(query, channel=channel, bot=bot)
        text = response.get("answer") or response.get("message", "")
        print(f"Channel: {channel}")
        print(f"Bot: {text}")
        print(f"Type: {response.get('type')} | Intent: {response.get('intent')}\n")


if __name__ == "__main__":
    run_demo()
