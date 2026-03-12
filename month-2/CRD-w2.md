# 📄 CRD — Component Requirements Document: Weeks 5–7

## Project: College FAQ Chatbot — Phase 2 (Smart Query Understanding)

---

## Component 6: Intent Training Data
**File:** `data/intents.json`
**Introduced in:** Week 5

| Attribute | Detail |
|-----------|--------|
| Format | JSON with `"intents"` array |
| Required intents | fees, exams, timetable, hostel, scholarships, admissions, contact |
| Min examples per intent | 15 sentences |
| Required fields | `tag`, `examples`, `description` |

**Acceptance Criteria:**
- At least 7 intents defined
- Each intent has ≥ 15 example sentences
- Example sentences are varied (not just rephrasing one sentence)

---

## Component 7: Intent Classifier
**File:** `utils/intent.py`
**Introduced in:** Week 5

| Function | Input | Output |
|----------|-------|--------|
| `train_classifier()` | `intents.json` | Saves model to `models/intent_model.pkl` |
| `predict_intent(query)` | Raw query string | Intent tag (string) |

**Model:** `Pipeline(TfidfVectorizer + LinearSVC)` — preferred for speed and accuracy

**Acceptance Criteria:**
- Train/test split accuracy ≥ 85%
- Model saved to disk after training
- `predict_intent("When is the exam?")` → `"exams"`
- Loads from disk on every call (no retraining)

---

## Component 8: Entity Extractor
**File:** `utils/entities.py`
**Introduced in:** Week 6

| Function | Input | Output |
|----------|-------|--------|
| `extract_entities(query)` | Raw query string | Dict with entity lists |

**Return structure (always):**
```python
{
    "dates": [],         # e.g., ["March 15th", "tomorrow"]
    "course_codes": [],  # e.g., ["CS301", "ME202"]
    "semester": []       # e.g., ["SEM 5", "third year"]
}
```

**Methods:**
- `spaCy en_core_web_sm` for date entities
- Custom regex for course codes: `r'\b[A-Z]{2,4}\s?\d{3}\b'`
- Custom regex for semesters: `r'\bSEM\s?\d\b'`

**Acceptance Criteria:**
- "When is the SEM 5 CS301 exam on March 15th?" returns all 3 entity types populated
- Always returns the full dict structure (no KeyErrors)

---

## Component 9: Context Manager
**File:** `utils/context.py`
**Introduced in:** Week 7

| Function | Input | Output |
|----------|-------|--------|
| `update_context(intent, entities)` | intent string, entities dict | Updates `st.session_state.context` |
| `resolve_context(query, intent, entities)` | current query data | Enriched intent + entities using history |
| `get_history()` | — | Last 3 conversation turns |

**Context stored in `st.session_state`:**
```python
{
    "last_intent": "exams",
    "last_entities": {"semester": ["SEM 5"]},
    "history": [{"user": "...", "bot": "..."}, ...]
}
```

**Acceptance Criteria:**
- "When is the exam?" followed by "What about third year?" correctly resolves to exam + sem 3
- History capped at last 3 turns
- Context resets cleanly on new session

---

## Component 10: Updated Streamlit UI (Phase 2)
**File:** `app.py` (updated)

| New UI Element | Description |
|----------------|-------------|
| Intent tag badge | Shows detected intent (e.g., "📌 exams") |
| Entities expander | Collapsible section showing extracted entities |
| Chat history panel | Last 3 messages in a scrollable container |

**Acceptance Criteria:**
- All Phase 1 features still working
- Intent and entities visible for every response
- Chat history displayed without page reload

---

## Dependencies Summary (New in Phase 2)
```
spacy
en_core_web_sm   # python -m spacy download en_core_web_sm
joblib
```
