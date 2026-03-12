"""
TF-IDF retrieval engine.

Uses TF-IDF vectorization and cosine similarity to find the
most relevant FAQ answer for a student query.

Introduced in: Week 4
"""

from typing import List, Dict, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.config import FALLBACK_ANSWER, EMPTY_QUERY_MSG
from src.core.preprocessor import preprocess
from src.core.synonyms import apply_synonyms


class TFIDFRetriever:
    """
    FAQ retrieval engine based on TF-IDF cosine similarity.

    Builds a TF-IDF matrix from FAQ questions, then finds the
    closest match for any incoming student query.
    """

    def __init__(self, faqs: List[Dict[str, str]]):
        """
        Initialize the retriever and build the TF-IDF index.

        Args:
            faqs: List of dicts with 'question' and 'answer' keys.
        """
        self.faqs = faqs
        self.vectorizer = TfidfVectorizer(sublinear_tf=True)

        # Preprocess + synonym-expand all FAQ questions for indexing
        self._processed_questions = [
            apply_synonyms(preprocess(faq["question"])) for faq in faqs
        ]

        # Build the TF-IDF matrix
        self.tfidf_matrix = self.vectorizer.fit_transform(self._processed_questions)

    def get_answer(self, query: str) -> Tuple[str, float]:
        """
        Find the best matching FAQ answer using cosine similarity.

        Args:
            query: Raw student question string.

        Returns:
            Tuple of (answer_text, confidence_score).
            Score is the cosine similarity between 0 and 1.
        """
        if not query or not query.strip():
            return EMPTY_QUERY_MSG, 0.0

        # Preprocess and apply synonyms to the query
        cleaned = apply_synonyms(preprocess(query))

        if not cleaned.strip():
            return EMPTY_QUERY_MSG, 0.0

        # Vectorize the query and compute cosine similarity
        query_vec = self.vectorizer.transform([cleaned])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Find the best match
        best_idx = similarities.argmax()
        best_score = float(similarities[best_idx])

        if best_score < 0.01:
            return FALLBACK_ANSWER, 0.0

        return self.faqs[best_idx]["answer"], round(best_score, 2)

    def get_top_n(self, query: str, n: int = 3) -> List[Tuple[str, str, float]]:
        """
        Return the top N matching FAQ answers.

        Args:
            query: Raw student question string.
            n: Number of top matches to return.

        Returns:
            List of (question, answer, score) tuples, sorted by score descending.
        """
        if not query or not query.strip():
            return []

        cleaned = apply_synonyms(preprocess(query))
        if not cleaned.strip():
            return []

        query_vec = self.vectorizer.transform([cleaned])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Get top N indices sorted by score
        top_indices = similarities.argsort()[::-1][:n]

        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score > 0.01:
                results.append((
                    self.faqs[idx]["question"],
                    self.faqs[idx]["answer"],
                    round(score, 2),
                ))

        return results
