"""
Text preprocessing module.

Cleans and normalizes raw user queries before they are passed
to the intent classifier or retrieval engine.
"""

import string
import nltk

# Ensure NLTK data is available
try:
    from nltk.corpus import stopwords
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords", quiet=True)
    nltk.download("punkt", quiet=True)

from nltk.corpus import stopwords

_stop_words = set(stopwords.words("english"))


def preprocess(text: str) -> str:
    """
    Clean and normalize a raw query string.

    Steps:
        1. Lowercase conversion
        2. Punctuation removal
        3. Stopword removal (NLTK English stopwords)

    Args:
        text: Raw query string.

    Returns:
        Cleaned, normalized string with stopwords and punctuation removed.
    """
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Tokenize and remove stopwords
    tokens = text.split()
    tokens = [w for w in tokens if w not in _stop_words]
    return " ".join(tokens)
