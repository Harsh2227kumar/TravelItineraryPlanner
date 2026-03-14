"""TF-IDF retrieval utility for weekly scripts."""

from typing import Dict, List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.preprocess import preprocess
from utils.synonyms import apply_synonyms


class TfidfFaqBot:
    """Retrieve FAQ answers via TF-IDF cosine similarity."""

    def __init__(self, faqs: List[Dict[str, str]]):
        """Build vector index from FAQ questions."""
        self._faqs = faqs
        self._vectorizer = TfidfVectorizer(sublinear_tf=True)
        self._questions = [apply_synonyms(preprocess(item["question"])) for item in faqs]
        self._matrix = self._vectorizer.fit_transform(self._questions)

    def get_answer(self, query: str) -> Tuple[str, float]:
        """Return best answer and confidence score in [0, 1]."""
        cleaned = apply_synonyms(preprocess(query))
        if not cleaned:
            return "Please ask a question about the college.", 0.0

        vector = self._vectorizer.transform([cleaned])
        similarities = cosine_similarity(vector, self._matrix).flatten()
        index = similarities.argmax()
        score = float(similarities[index])
        return self._faqs[index]["answer"], round(score, 2)

    def get_top_n(self, query: str, n: int = 3) -> List[Tuple[str, str, float]]:
        """Return top N matching FAQ rows as (question, answer, score)."""
        cleaned = apply_synonyms(preprocess(query))
        if not cleaned:
            return []

        vector = self._vectorizer.transform([cleaned])
        similarities = cosine_similarity(vector, self._matrix).flatten()
        indices = similarities.argsort()[::-1][:n]
        return [
            (self._faqs[i]["question"], self._faqs[i]["answer"], round(float(similarities[i]), 2))
            for i in indices
        ]
