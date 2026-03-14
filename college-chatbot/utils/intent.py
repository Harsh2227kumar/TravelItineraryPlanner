"""Intent model utility for weekly scripts."""

from pathlib import Path
from typing import Dict, List, Tuple

import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score

from utils.data import load_intents

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "intent_model_weeks.pkl"
REQUIRED_INTENTS = [
    "fees",
    "exams",
    "timetable",
    "hostel",
    "scholarships",
    "admissions",
    "contact",
]


def _build_dataset() -> Tuple[List[str], List[str]]:
    """Build training X/y from only required month-2 intents."""
    data = load_intents()
    rows = [intent for intent in data["intents"] if intent["tag"] in REQUIRED_INTENTS]
    X: List[str] = []
    y: List[str] = []
    for intent in rows:
        for sample in intent["examples"]:
            X.append(sample)
            y.append(intent["tag"])
    return X, y


def train_classifier() -> Dict:
    """Train and persist week-track intent classifier."""
    X, y = _build_dataset()
    model = Pipeline([
        ("tfidf", TfidfVectorizer(sublinear_tf=True, ngram_range=(1, 2))),
        ("clf", LinearSVC(dual=False, C=0.5, max_iter=10000)),
    ])

    cv_scores = cross_val_score(model, X, y, cv=3, scoring="accuracy")
    model.fit(X, y)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return {"accuracy": float(cv_scores.mean()), "cv_scores": cv_scores.tolist()}


def predict_intent(query: str) -> str:
    """Predict intent label from query text."""
    model = joblib.load(MODEL_PATH)
    return model.predict([query])[0]
