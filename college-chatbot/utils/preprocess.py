"""Text preprocessing utility for weekly scripts."""

import string
import nltk

try:
    from nltk.corpus import stopwords
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords", quiet=True)

from nltk.corpus import stopwords

_STOP_WORDS = set(stopwords.words("english"))


def preprocess(text: str) -> str:
    """Lowercase, remove punctuation, and drop stopwords."""
    cleaned = text.lower().translate(str.maketrans("", "", string.punctuation))
    tokens = [token for token in cleaned.split() if token not in _STOP_WORDS]
    return " ".join(tokens)
