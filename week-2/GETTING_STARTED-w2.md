# 🚀 Getting Started — Weeks 5–7: Smart Query Understanding

## What You're Building
Upgrading your FAQ chatbot with intent classification, entity extraction, and multi-turn conversation support — so it truly understands what a student is asking.

---

## New Tech Added This Phase
| Tool | Purpose |
|------|---------|
| scikit-learn | Intent classifier (Naive Bayes / SVM) |
| spaCy | Entity recognition (dates, course codes) |
| Python dict / list | Conversation state management |
| Streamlit session_state | Multi-turn context in UI |

---

## Folder Structure (Updated)
```
college-chatbot/
│
├── data/
│   ├── faqs.json
│   └── intents.json         # Intent training data (NEW)
│
├── weeks/
│   ├── week5_intent_classifier.py
│   ├── week6_entity_extractor.py
│   └── week7_context_handler.py
│
├── models/
│   └── intent_model.pkl     # Saved trained classifier
│
├── app.py                   # Updated Streamlit UI
└── requirements.txt
```

---

## New Installation Steps

```bash
# spaCy + English model
pip install spacy
python -m spacy download en_core_web_sm

# joblib for saving model
pip install joblib
```

---

## Week-by-Week Kickoff

### Week 5 — Intent Classification
- Define 5–7 intents: `admissions`, `exams`, `timetable`, `hostel`, `scholarships`, `fees`, `contact`
- Create training sentences for each intent in `intents.json`
- Train a `MultinomialNB` or `LinearSVC` classifier
- Route queries to the right intent bucket before answering

### Week 6 — Entity Extraction
- Use spaCy to extract:
  - Dates → e.g., "exam on 15th March"
  - Course codes → e.g., "CS301", "SEM 5"
  - Semester numbers → e.g., "third year", "semester 6"
- Use extracted entities to personalize responses

### Week 7 — Context Handling for Follow-ups
- Track last intent + entities in `st.session_state`
- If next query is vague (e.g., "What about third year?"), resolve it using previous context
- Maintain a minimal conversation history (last 2–3 turns)

---

## Key Concept: How These 3 Weeks Connect
```
Student Query
     ↓
[Week 2] Preprocess
     ↓
[Week 5] Classify Intent → which topic?
     ↓
[Week 6] Extract Entities → which course/date/sem?
     ↓
[Week 7] Check Context → is this a follow-up?
     ↓
Fetch Answer from FAQ DB
```

---

## First Thing To Do Right Now
1. Create `intents.json` with 10+ example sentences per intent
2. Train your classifier in `week5_intent_classifier.py`
3. Test with: "When is the SEM 5 CS exam?" → should detect intent=`exams`, entity=`SEM 5, CS`
