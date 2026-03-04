# 🚀 Getting Started — Weeks 8–10: Production Ready

## What You're Building
Making your chatbot robust, deployable, and self-improving — with fallback handling, multi-channel mockups, and analytics to keep getting better.

---

## New Tech Added This Phase
| Tool | Purpose |
|------|---------|
| Streamlit | Web channel (already have) |
| Python logging / SQLite | Interaction logging |
| pandas | Analytics & pattern analysis |
| Twilio / CLI mock | WhatsApp / mobile mockup |
| matplotlib / plotly | Analytics dashboard |

---

## Folder Structure (Final)
```
college-chatbot/
│
├── data/
│   ├── faqs.json
│   ├── intents.json
│   └── logs/
│       └── interactions.db      # SQLite log database (NEW)
│
├── weeks/
│   ├── week8_fallback.py
│   ├── week9_multichannel.py
│   └── week10_analytics.py
│
├── channels/
│   ├── web_app.py               # Streamlit (web)
│   ├── cli_app.py               # Console/mobile mock
│   └── whatsapp_mock.py         # WhatsApp logic mock
│
├── analytics/
│   └── dashboard.py             # Streamlit analytics page
│
├── app.py
└── requirements.txt
```

---

## New Installation Steps

```bash
pip install plotly sqlite3
# sqlite3 is built into Python — no extra install needed
```

---

## Week-by-Week Kickoff

### Week 8 — Fallbacks and Handover
- Define confidence threshold (e.g., similarity score < 0.3 = fallback)
- On fallback: ask clarifying question OR suggest top 3 related FAQs
- Add "Talk to Advisor" button in Streamlit → mailto link or desk contact

### Week 9 — Multichannel Deployment Mockup
- **Web** → already working via Streamlit
- **CLI** → `cli_app.py` simulates mobile app (same logic, terminal I/O)
- **WhatsApp** → `whatsapp_mock.py` simulates message in/out (no real API needed)
- All 3 channels use the same core chatbot logic — only I/O layer changes

### Week 10 — Analytics and Continuous Improvement
- Log every interaction: query, detected intent, confidence, answer given, timestamp
- Label a sample of unanswered/low-confidence queries
- Generate a report: top 10 unhandled questions, weak intents, suggested new FAQs
- Display analytics in a Streamlit dashboard page

---

## First Thing To Do Right Now
1. Create `logs/interactions.db` with SQLite
2. Add logging calls into your existing `app.py`
3. Build the fallback logic in `week8_fallback.py`
