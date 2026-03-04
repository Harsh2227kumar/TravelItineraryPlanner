"""
Intent classification engine.

Trains a TF-IDF + classifier pipeline on intent examples from intents.json,
saves the model to disk, and provides a prediction function.
"""

import json

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report

from src.config import INTENTS_PATH, INTENT_MODEL_PATH


def _load_training_data():
    """Load intent examples from intents.json and return (X, y) lists."""
    with open(INTENTS_PATH, encoding="utf-8") as f:
        data = json.load(f)

    X, y = [], []
    for intent in data["intents"]:
        for example in intent["examples"]:
            X.append(example)
            y.append(intent["tag"])
    return X, y


def train_classifier(test_size: float = 0.2) -> dict:
    """
    Train the intent classifier and save to disk.

    Uses cross-validation for robust accuracy measurement, then
    trains the final model on the full dataset for best quality.

    Args:
        test_size: Not used directly — kept for API compatibility.

    Returns:
        Dict with 'accuracy' and 'report' from cross-validation.
    """
    X, y = _load_training_data()

    model = Pipeline([
        ("tfidf", TfidfVectorizer(sublinear_tf=True)),
        ("clf", MultinomialNB(alpha=0.1)),
    ])

    # Cross-validation for robust accuracy estimate
    cv_scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
    accuracy = cv_scores.mean()

    # Train on FULL dataset for the saved model
    model.fit(X, y)

    # Generate classification report on training data (for reference)
    y_pred = model.predict(X)
    report = classification_report(y, y_pred, zero_division=0)

    # Save model
    INTENT_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, INTENT_MODEL_PATH)

    return {"accuracy": accuracy, "report": report, "cv_scores": cv_scores.tolist()}


# ── Cached model for predictions ─────────────────────────────────────────────
_model = None


def _get_model():
    """Load the saved model from disk (cached after first call)."""
    global _model
    if _model is None:
        if not INTENT_MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Intent model not found at {INTENT_MODEL_PATH}. "
                "Run `python train.py` first to train the classifier."
            )
        _model = joblib.load(INTENT_MODEL_PATH)
    return _model


def predict_intent(query: str) -> str:
    """
    Predict the intent of a raw query string.

    Args:
        query: Raw user question.

    Returns:
        Intent tag string (e.g., 'exams', 'fees').
    """
    model = _get_model()
    return model.predict([query])[0]

