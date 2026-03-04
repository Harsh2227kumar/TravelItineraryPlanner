"""
Train the intent classifier.

Run this script once to train and save the model:
    python train.py

The saved model is used at runtime by src.core.intent.predict_intent().
"""

import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.intent import train_classifier  # noqa: E402


def main():
    print("=" * 55)
    print("  🎓  College FAQ Chatbot — Intent Classifier Trainer")
    print("=" * 55)
    print()

    print("Training classifier...")
    result = train_classifier(test_size=0.2)

    print(f"\n✅ Training complete!")
    print(f"   Accuracy: {result['accuracy']:.1%}")
    print(f"\nClassification Report:")
    print(result["report"])

    if result["accuracy"] >= 0.85:
        print("🟢 Accuracy meets the 85% threshold — model is ready!")
    else:
        print("🟡 Accuracy below 85% — consider adding more training examples.")


if __name__ == "__main__":
    main()
