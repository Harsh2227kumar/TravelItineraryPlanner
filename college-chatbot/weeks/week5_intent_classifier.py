"""Week 5: Intent classifier training and prediction demo."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.intent import train_classifier, predict_intent


def run_demo():
    """Train the intent model and run a few sample predictions."""
    print("Week 5 - Intent Classification")
    result = train_classifier()
    print(f"Training complete. CV Accuracy: {result['accuracy']:.2%}\n")

    samples = [
        "What is the hostel fee?",
        "When are semester exams?",
        "How do I contact admission office?",
    ]
    for query in samples:
        intent = predict_intent(query)
        print(f"Query: {query}")
        print(f"Intent: {intent}\n")


if __name__ == "__main__":
    run_demo()
