# 🎨 DESIGN — Architecture & UI: Weeks 8–10

## Final System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CHANNELS                             │
│  ┌───────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │  Web (Streamlit│  │  CLI (mobile │  │  WhatsApp Mock  │  │
│  │  web_app.py)  │  │  cli_app.py) │  │  whatsapp_mock) │  │
│  └───────┬───────┘  └──────┬───────┘  └────────┬────────┘  │
└──────────┼─────────────────┼───────────────────┼────────────┘
           └─────────────────┼───────────────────┘
                             │ chat(user_input)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    core_bot.py                              │
│                                                             │
│  preprocess → predict_intent → extract_entities             │
│       → resolve_context → handle_response → log_interaction │
└──────────────────────────────┬──────────────────────────────┘
                               │
           ┌───────────────────┼───────────────────┐
           ▼                   ▼                   ▼
  utils/fallback.py    utils/retrieval.py   utils/logger.py
           │                                       │
           ▼                                       ▼
  data/faqs.json                      data/logs/interactions.db
```

---

## Fallback Decision Tree

```
get_answer(query) returns (answer, score)
        │
        ├── score > 0.3 ──────────────────────────▶ ✅ Return answer
        │
        ├── 0.2 ≤ score ≤ 0.3 ─────────────────▶ ⚠️ Soft Fallback
        │        │                                    Show top 3 FAQs
        │        │                                    Ask clarifying Q
        │        │                                    Show advisor link
        │
        └── score < 0.2 ──────────────────────▶ ❌ Hard Fallback
                                                    "I couldn't find..."
                                                    Show advisor contact
                                                    Log as unhandled
```

---

## Multichannel Architecture

```
                    ┌──────────────────┐
                    │   core_bot.py    │
                    │  chat(input)     │
                    └────────┬─────────┘
                             │ same function
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │  web_app.py  │  │  cli_app.py  │  │whatsapp_mock │
  │              │  │              │  │              │
  │  Streamlit   │  │  print()     │  │  [WA] format │
  │  st.write()  │  │  input()     │  │  input()     │
  └──────────────┘  └──────────────┘  └──────────────┘
```

---

## Analytics Data Flow

```
Every chat() call
        │
        ▼
log_interaction(query, intent, confidence, answer, was_fallback)
        │
        ▼
interactions.db (SQLite)
        │
        ▼
analytics/dashboard.py reads DB via get_logs_df()
        │
        ├── Queries over time chart (plotly line)
        ├── Intent distribution chart (plotly bar)
        ├── Fallback rate metric (st.metric)
        └── Top unhandled queries table (st.dataframe)
```

---

## Final UI Design

### Main App (web_app.py)
```
┌──────────────────────────────────────────────────────────┐
│  🎓 College FAQ Chatbot              [Sidebar ▶]         │
├──────────────────────────────────────────────────────────┤
│  💬 Chat History                                         │
│  ┌────────────────────────────────────────────────────┐  │
│  │ You: what about hostel fees                        │  │
│  │ 🤖 Bot: Hostel fee is ₹40,000/year incl. meals.   │  │
│  │         📌 exams  |  🟢 0.81  |  Semester: SEM 3  │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  [Type your question...]            [Send]               │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Fallback UI
```
┌────────────────────────────────────────────────┐
│  ⚠️ I'm not sure about that. Did you mean:     │
│                                                │
│  1. What is the hostel fee?                    │
│  2. What are the hostel rules?                 │
│  3. How to apply for hostel?                   │
│                                                │
│  📞 [Talk to an Advisor →]                     │
└────────────────────────────────────────────────┘
```

### Analytics Dashboard (analytics/dashboard.py)
```
┌──────────────────────────────────────────────────────────┐
│  📊 Chatbot Analytics Dashboard                          │
├─────────────────┬────────────────┬───────────────────────┤
│ Total Queries   │ Fallback Rate  │ Top Intent            │
│     1,247       │    12.3%       │    exams (34%)        │
├─────────────────┴────────────────┴───────────────────────┤
│ 📈 Queries Over Time (line chart)                        │
│ 🥧 Intent Distribution (bar chart)                       │
│ 📋 Top Unhandled Queries (table)                         │
│ 💡 Improvement Proposals (text section)                  │
└──────────────────────────────────────────────────────────┘
```

---

## Design Decisions Log

| Decision | Why |
|----------|-----|
| SQLite over CSV for logs | Structured queries, filtering, aggregation for analytics |
| Two-level fallback (soft/hard) | Soft fallback keeps conversation alive; hard fallback escalates gracefully |
| CLI channel uses same `core_bot.py` | Ensures consistent behavior; avoids code duplication |
| Plotly for analytics charts | Interactive, renders natively in Streamlit, no extra setup |
| Advisor link as mailto | Simple, universally supported, no backend needed |
| `was_fallback` as 0/1 integer | Easy to compute fallback rate with SQL `AVG(was_fallback)` |
