# ⚡ Quick Reference — Weeks 5–7

## Run Commands
```bash
streamlit run app.py                        # Full UI
python weeks/week5_intent_classifier.py    # Train & test classifier
python weeks/week6_entity_extractor.py     # Test entity extraction
python weeks/week7_context_handler.py      # Test multi-turn logic
```

---

## Key Code Snippets

### intents.json Format
```json
{
  "intents": [
    {
      "tag": "fees",
      "examples": ["What is the fee?", "How much does it cost?", "tuition amount"]
    },
    {
      "tag": "exams",
      "examples": ["When is the exam?", "exam schedule", "SEM 5 exam date"]
    }
  ]
}
```

### Train Intent Classifier (Week 5)
```python
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib, json

with open("data/intents.json") as f:
    data = json.load(f)

X, y = [], []
for intent in data["intents"]:
    for ex in intent["examples"]:
        X.append(ex)
        y.append(intent["tag"])

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf",   LinearSVC())
])
model.fit(X, y)
joblib.dump(model, "models/intent_model.pkl")

def predict_intent(query):
    model = joblib.load("models/intent_model.pkl")
    return model.predict([query])[0]
```

### Entity Extraction with spaCy (Week 6)
```python
import spacy, re
nlp = spacy.load("en_core_web_sm")

def extract_entities(query):
    doc = nlp(query)
    entities = {}
    # Dates
    entities["dates"] = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    # Course codes (custom regex)
    entities["course_codes"] = re.findall(r'\b[A-Z]{2,4}\s?\d{3}\b', query)
    # Semester numbers
    entities["semester"] = re.findall(r'\bSEM\s?\d\b|\b[Ss]emester\s\d\b', query)
    return entities
```

### Context Handling in Streamlit (Week 7)
```python
import streamlit as st

# Initialize session state
if "context" not in st.session_state:
    st.session_state.context = {"last_intent": None, "last_entities": {}}

def resolve_with_context(query, intent, entities):
    # If current query is vague, use previous context
    if not intent or intent == "unknown":
        intent = st.session_state.context["last_intent"]
    if not entities.get("semester"):
        entities["semester"] = st.session_state.context["last_entities"].get("semester")
    # Update context
    st.session_state.context = {"last_intent": intent, "last_entities": entities}
    return intent, entities
```

---

## Common Errors & Fixes
| Error | Fix |
|-------|-----|
| `OSError: [E050] Can't find model 'en_core_web_sm'` | `python -m spacy download en_core_web_sm` |
| Low classifier accuracy | Add more training examples per intent (aim for 15+) |
| Context not persisting between messages | Make sure you're using `st.session_state` not regular variables |
| `ModuleNotFoundError: joblib` | `pip install joblib` |
