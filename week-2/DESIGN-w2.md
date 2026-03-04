# 🎨 DESIGN — Architecture & UI: Weeks 5–7

## System Architecture (Updated)

```
┌──────────────────────────────────────────────────────┐
│                Streamlit Web UI (app.py)              │
│  ┌──────────┐   ┌──────────────────────────────────┐ │
│  │  Input   │   │ Chat History (last 3 turns)      │ │
│  └──────────┘   │ Intent Badge | Entities Panel    │ │
│                 └──────────────────────────────────┘ │
└─────────────────────────┬────────────────────────────┘
                          │ query
                          ▼
┌──────────────────────────────────────────────────────┐
│                   Bot Logic Layer                    │
│                                                      │
│  1. preprocess(query)          [utils/preprocess.py] │
│        ↓                                             │
│  2. apply_synonyms(query)      [utils/synonyms.py]   │
│        ↓                                             │
│  3. predict_intent(query)      [utils/intent.py]     │
│        ↓                                             │
│  4. extract_entities(query)    [utils/entities.py]   │
│        ↓                                             │
│  5. resolve_context(...)       [utils/context.py]    │
│        ↓                                             │
│  6. get_answer(query, intent)  [utils/retrieval.py]  │
└─────────────────────────┬────────────────────────────┘
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
    data/faqs.json  data/intents.json  models/intent_model.pkl
```

---

## Intent Classification Flow

```
Raw Query
    │
    ▼
Preprocess → "sem 5 exam date"
    │
    ▼
TF-IDF Vectorize
    │
    ▼
LinearSVC Predict → "exams"
    │
    ▼
Route to exam FAQs subset → better answer retrieval
```

---

## Entity Extraction Flow

```
Raw Query: "When is the SEM 5 CS301 exam on March 15th?"
    │
    ├── spaCy NER → dates: ["March 15th"]
    ├── regex     → course_codes: ["CS301"]
    └── regex     → semester: ["SEM 5"]
    │
    ▼
Personalized Response:
"The CS301 exam for SEM 5 is scheduled on March 15th."
```

---

## Context Resolution Flow

```
Turn 1: "When is the exam?" → intent=exams, entities={}
         Bot: "Which exam? Please specify semester or course."

Turn 2: "For third year students"
         ↓
    resolve_context():
         last_intent = "exams"  ← from session_state
         current_entities = {semester: ["third year"]}
         ↓
    Final: intent=exams, semester=third year → correct answer
```

---

## Module Dependency Map (Updated)

```
app.py
 ├── core_bot.py (being introduced)
 │    ├── utils/preprocess.py
 │    ├── utils/synonyms.py
 │    ├── utils/intent.py          ← NEW (Week 5)
 │    ├── utils/entities.py        ← NEW (Week 6)
 │    ├── utils/context.py         ← NEW (Week 7)
 │    └── utils/retrieval.py
 └── data/
      ├── faqs.json
      └── intents.json             ← NEW (Week 5)
```

---

## UI Design (Updated)

### Main Screen Layout
```
┌─────────────────────────────────────────────────────┐
│  🎓 College FAQ Chatbot              [Sidebar ▶]   │
├─────────────────────────────────────────────────────┤
│  💬 Chat History                                    │
│  ┌───────────────────────────────────────────────┐  │
│  │ You: When is the exam?                        │  │
│  │ Bot: Which exam? Specify course or semester.  │  │
│  │ You: For SEM 5 CS301                          │  │
│  │ Bot: CS301 exam is on March 15th, 10am.       │  │
│  └───────────────────────────────────────────────┘  │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │ 💬 Type your question...                      │  │
│  └───────────────────────────────────────────────┘  │
│                                                     │
│  📌 Intent: exams    Confidence: 0.81 🟢           │
│  ▼ Entities detected                               │
│    • Semester: SEM 5                               │
│    • Course: CS301                                 │
│    • Date: March 15th                              │
└─────────────────────────────────────────────────────┘
```

### Sidebar Layout (Updated)
```
┌──────────────────────────┐
│  ℹ️ About                │
│  Phase 2 (Wk 5–7)        │
│                          │
│  🎯 Intents:             │
│  • fees                  │
│  • exams                 │
│  • timetable             │
│  • hostel                │
│  • scholarships          │
│  • admissions            │
│  • contact               │
│                          │
│  🔄 [Clear Context]      │
└──────────────────────────┘
```

---

## Design Decisions Log

| Decision | Why |
|----------|-----|
| LinearSVC over Naive Bayes | Better performance on short text with small datasets |
| spaCy for dates, regex for codes | spaCy handles natural date expressions; regex better for structured codes like "CS301" |
| `st.session_state` for context | Only option for persistent state across Streamlit reruns |
| Show entities in collapsible expander | Keeps UI clean; devs/evaluators can expand to verify |
| Cap context at 3 turns | Longer context adds complexity without benefit for college FAQ scope |
