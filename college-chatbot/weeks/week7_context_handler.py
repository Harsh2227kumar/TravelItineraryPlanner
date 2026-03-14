"""Week 7: Context handling demo."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.context import ContextManager
from utils.entities import extract_entities
from utils.intent import predict_intent, train_classifier


def run_demo():
    """Run a multi-turn demo with explicit context resolution."""
    print("Week 7 - Context Handling for Follow-ups")
    train_classifier()
    context = ContextManager(max_turns=3)

    conversation = [
        "When are the semester exams?",
        "What about SEM 5?",
        "And CS301?",
    ]

    for query in conversation:
        intent = predict_intent(query)
        entities = extract_entities(query)
        resolved_intent, resolved_entities = context.resolve(intent, entities)
        text = f"Resolved intent={resolved_intent}, entities={resolved_entities}"

        context.update(query, text, resolved_intent, resolved_entities)

        print(f"You: {query}")
        print(f"Bot: {text}")
        print(f"History size: {len(context.history)}\n")


if __name__ == "__main__":
    run_demo()
