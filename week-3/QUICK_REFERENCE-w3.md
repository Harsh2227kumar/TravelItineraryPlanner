# ⚡ Quick Reference — Weeks 8–10

## Run Commands
```bash
streamlit run app.py                    # Web channel (main app)
python channels/cli_app.py             # CLI/mobile mock
python channels/whatsapp_mock.py       # WhatsApp mock
streamlit run analytics/dashboard.py  # Analytics dashboard
python weeks/week10_analytics.py       # Generate improvement report
```

---

## Key Code Snippets

### Fallback Strategy (Week 8)
```python
CONFIDENCE_THRESHOLD = 0.3

def get_response_with_fallback(query):
    answer, score = get_answer(query)   # from Week 4 TF-IDF

    if score < CONFIDENCE_THRESHOLD:
        # Option 1: Ask for clarification
        clarification = "I'm not sure I understood. Are you asking about fees, exams, or timetable?"
        # Option 2: Suggest top 3 related FAQs
        top3 = get_top_n_answers(query, n=3)
        return {"type": "fallback", "clarification": clarification, "suggestions": top3}

    return {"type": "answer", "answer": answer, "score": score}
```

### Streamlit Fallback UI (Week 8)
```python
result = get_response_with_fallback(user_input)

if result["type"] == "fallback":
    st.warning("🤔 I'm not sure about that. Did you mean:")
    for i, suggestion in enumerate(result["suggestions"]):
        st.write(f"{i+1}. {suggestion['question']}")
    st.info("📞 [Contact an Advisor](mailto:advisor@college.edu)")
else:
    st.write(result["answer"])
```

### Log Interactions to SQLite (Week 10)
```python
import sqlite3, datetime

def init_db():
    conn = sqlite3.connect("data/logs/interactions.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT, query TEXT, intent TEXT,
        confidence REAL, answer TEXT, was_fallback INTEGER
    )""")
    conn.commit(); conn.close()

def log_interaction(query, intent, confidence, answer, was_fallback):
    conn = sqlite3.connect("data/logs/interactions.db")
    conn.execute("INSERT INTO logs VALUES (NULL,?,?,?,?,?,?)",
        (str(datetime.datetime.now()), query, intent, confidence, answer, int(was_fallback)))
    conn.commit(); conn.close()
```

### Analytics: Top Unhandled Queries (Week 10)
```python
import pandas as pd, sqlite3

def get_analytics():
    conn = sqlite3.connect("data/logs/interactions.db")
    df = pd.read_sql("SELECT * FROM logs", conn)
    conn.close()

    fallbacks = df[df["was_fallback"] == 1]
    top_unhandled = fallbacks["query"].value_counts().head(10)
    weak_intents  = df.groupby("intent")["confidence"].mean().sort_values()
    return top_unhandled, weak_intents
```

### Channel-Agnostic Core (Week 9)
```python
# core_bot.py — same logic, used by all channels
def chat(user_input):
    processed = preprocess(user_input)
    intent    = predict_intent(processed)
    entities  = extract_entities(user_input)
    result    = get_response_with_fallback(processed)
    log_interaction(user_input, intent, result.get("score", 0),
                    result.get("answer", ""), result["type"] == "fallback")
    return result
```

---

## Common Errors & Fixes
| Error | Fix |
|-------|-----|
| `sqlite3.OperationalError: no such table` | Run `init_db()` once before logging |
| Analytics dashboard is empty | Make sure interactions have been logged first |
| CLI app crashes | Check that `core_bot.py` is imported correctly |
| Confidence always 0 | Ensure TF-IDF matrix is fitted before querying |
