# ⚡ Quick Reference — Weeks 1–4

## Run Commands
```bash
streamlit run app.py                    # Run full Streamlit UI
python weeks/week1_basic_bot.py         # Run Week 1 standalone
python weeks/week2_preprocessing.py    # Run Week 2 standalone
python weeks/week3_synonym_bot.py      # Run Week 3 standalone
python weeks/week4_tfidf_bot.py        # Run Week 4 standalone
```

---

## Key Code Snippets

### Load FAQs from JSON
```python
import json
with open("data/faqs.json") as f:
    faqs = json.load(f)
# faqs = [{"question": "...", "answer": "..."}, ...]
```

### Preprocessing Pipeline (Week 2)
```python
import nltk, string
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    tokens = [w for w in tokens if w not in stop_words]
    return " ".join(tokens)
```

### Synonym Mapping (Week 3)
```python
synonyms = {
    "tuition": "fees", "payment": "fees", "cost": "fees",
    "schedule": "timetable", "timing": "timetable",
    "contact": "office", "reach": "office"
}

def apply_synonyms(text):
    words = text.split()
    return " ".join([synonyms.get(w, w) for w in words])
```

### TF-IDF Matching (Week 4)
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

questions = [faq["question"] for faq in faqs]
answers   = [faq["answer"]   for faq in faqs]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(questions)

def get_answer(user_query):
    query_vec = vectorizer.transform([preprocess(user_query)])
    scores = cosine_similarity(query_vec, tfidf_matrix)[0]
    best_idx = np.argmax(scores)
    return answers[best_idx], scores[best_idx]
```

### Basic Streamlit UI
```python
import streamlit as st

st.title("🎓 College FAQ Chatbot")
user_input = st.text_input("Ask your question:")
if user_input:
    answer, score = get_answer(user_input)
    st.write(f"**Answer:** {answer}")
    st.caption(f"Confidence: {score:.2f}")
```

---

## faqs.json Format
```json
[
  {"question": "What are the college timings?", "answer": "College is open 8am to 5pm."},
  {"question": "What is the fee for B.Tech?",   "answer": "B.Tech fee is ₹80,000/year."}
]
```

---

## Common Errors & Fixes
| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: nltk` | `pip install nltk` |
| `LookupError: stopwords` | `nltk.download('stopwords')` |
| TF-IDF returns wrong answer | Add more FAQ entries, check preprocessing |
| Streamlit not found | `pip install streamlit` |
