# 📋 Rules — Weeks 5–7: Smart Query Understanding

## Code Rules

### R1 — Modular Architecture is Mandatory
Intent classification, entity extraction, and context handling must each be in their own file. No monolithic scripts.
```
utils/intent.py      ← Week 5
utils/entities.py    ← Week 6
utils/context.py     ← Week 7
```

### R2 — Classifier Must Be Saved and Loaded, Not Retrained Every Run
Train the model once, save it with `joblib`, and load it in the app. Do not retrain on every Streamlit page refresh.

### R3 — Training Data Must Be in intents.json
Never hardcode training sentences in Python. All intent examples live in `data/intents.json`.

### R4 — Minimum Training Examples Per Intent
Each intent must have **at least 15 example sentences** before training. Less than 10 will produce unreliable results.

### R5 — Entity Extractor Must Return a Dict
`extract_entities()` must always return a dictionary with consistent keys, even if values are empty lists.
```python
# Always return this structure:
{"dates": [], "course_codes": [], "semester": []}
```

---

## Intent Rules

### R6 — Define Exactly 5–7 Intents
Stick to: `fees`, `exams`, `timetable`, `hostel`, `scholarships`, `admissions`, `contact`. Do not create more than 7 intents in this phase.

### R7 — Intents Must Not Overlap
Each intent must have clearly distinct example sentences. Overlapping training data causes classifier confusion.

### R8 — Test Accuracy Before Moving On
Run a quick train/test split (80/20). Intent accuracy must be above **85%** before integrating into the main app.

---

## Context Rules

### R9 — Context Lives in session_state Only
Conversation context must be stored in `st.session_state`. Never use global variables for this — they don't persist correctly in Streamlit.

### R10 — Context Window is Max 3 Turns
Only keep the last 3 conversation turns in context. Don't grow context indefinitely.

### R11 — Vague Queries Must Explicitly Fall Back to Context
If a query has no clear intent, the system must explicitly check context before returning "I don't know."

---

## UI Rules

### R12 — Show Intent and Entities in UI
The Streamlit interface must display detected intent and extracted entities below the answer (can be in an expander/collapsible).

### R13 — Chat History Must Be Visible
Display the last 3–5 messages in a chat-style history in the UI.

---

## Submission Rules

### R14 — Model File Must Be Gitignored or Included Intentionally
Either include `models/intent_model.pkl` or provide a `train.py` script the evaluator can run to regenerate it.

### R15 — Document Each Intent
In `intents.json`, every intent tag must have a `"description"` field explaining what it covers.
