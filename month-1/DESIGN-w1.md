# 🎨 DESIGN — Architecture & UI: Weeks 1–4

## System Architecture

```
┌─────────────────────────────────────────┐
│           Streamlit Web UI (app.py)     │
│  ┌─────────────┐    ┌────────────────┐  │
│  │ Text Input  │───▶│  Chat Window   │  │
│  └─────────────┘    └────────────────┘  │
└───────────────────────┬─────────────────┘
                        │ query
                        ▼
┌─────────────────────────────────────────┐
│             Bot Logic Layer             │
│                                         │
│  1. preprocess(query)                   │
│        ↓                                │
│  2. apply_synonyms(query)               │
│        ↓                                │
│  3. get_answer(query)  ◀── TF-IDF       │
│        ↓                                │
│  returns (answer, score)                │
└───────────────────────┬─────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────┐
│              Data Layer                 │
│         data/faqs.json                  │
│   [{"question": ..., "answer": ...}]    │
└─────────────────────────────────────────┘
```

---

## Data Flow — Step by Step

1. Student types a question in Streamlit text input
2. `preprocess()` cleans the query (lowercase, no stopwords, no punctuation)
3. `apply_synonyms()` maps variant words to canonical keywords
4. `TfidfVectorizer` converts the query to a vector
5. `cosine_similarity` finds the closest FAQ question vector
6. The matched answer + confidence score is returned to the UI

---

## Module Dependency Map

```
app.py
 ├── utils/preprocess.py     (Week 2)
 ├── utils/synonyms.py       (Week 3)
 ├── utils/retrieval.py      (Week 4)
 │    └── uses preprocess.py + synonyms.py internally
 └── data/faqs.json          (Week 1)
```

---

## UI Design

### Main Screen Layout
```
┌──────────────────────────────────────────────┐
│  🎓 College FAQ Chatbot          [Sidebar ▶] │
├──────────────────────────────────────────────┤
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │ 💬 Ask your question here...          │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │ 🤖 Answer:                            │  │
│  │ College timings are 8 AM to 5 PM.     │  │
│  │                                        │  │
│  │ Confidence: ████████░░ 0.78 ✅        │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

### Sidebar Layout
```
┌──────────────────────┐
│  ℹ️ About            │
│  College FAQ Bot     │
│  Phase 1 (Wk 1–4)   │
│                      │
│  📚 Topics covered:  │
│  • Fees              │
│  • Timings           │
│  • Exams             │
│  • Contacts          │
│  • Hostel            │
└──────────────────────┘
```

---

## Color Coding for Confidence Score
| Score Range | Color | Meaning |
|-------------|-------|---------|
| > 0.5 | 🟢 Green | High confidence |
| 0.3 – 0.5 | 🟡 Yellow | Medium confidence |
| < 0.3 | 🔴 Red | Low confidence (future: fallback) |

---

## Streamlit UI Code Pattern
```python
# Confidence color logic
def confidence_color(score):
    if score > 0.5:   return "🟢"
    elif score > 0.3: return "🟡"
    else:             return "🔴"
```

---

## Design Decisions Log

| Decision | Why |
|----------|-----|
| Use JSON over CSV for FAQs | Easier to add metadata fields later (category, week) |
| TF-IDF over embeddings | Simpler, faster, no GPU needed, perfect for college FAQ scale |
| Streamlit over Flask | No HTML/CSS needed, fast prototyping, good for submission demos |
| Preprocessing before TF-IDF | Reduces vocabulary noise and improves similarity accuracy |
