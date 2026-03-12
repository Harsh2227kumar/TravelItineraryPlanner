# 📋 Rules — Weeks 8–10: Production Ready

## Code Rules

### R1 — Core Bot Logic Must Be Channel-Agnostic
All chatbot logic lives in `core_bot.py`. Channel files (web, CLI, WhatsApp) only handle input/output — they must NOT contain any chatbot logic.

### R2 — Confidence Threshold Must Be a Named Constant
```python
CONFIDENCE_THRESHOLD = 0.3  # in core_bot.py or config.py
```
Never hardcode `0.3` in multiple places. One constant, one place.

### R3 — Every Interaction Must Be Logged
No exceptions. Every query that hits the bot — answered or fallback — must be logged to the SQLite database with timestamp, intent, confidence, and whether it was a fallback.

### R4 — Fallback Must Always Offer Options
A fallback response must never be a dead end. It must always include at least one of:
- A clarifying question
- Top 3 related FAQ suggestions
- A link/button to contact a human advisor

### R5 — Analytics Must Use Real Logged Data
The analytics dashboard must query from `interactions.db`. Do not use fake/hardcoded data in the dashboard.

---

## Fallback Rules

### R6 — Two-Level Fallback Strategy
1. **Level 1** (score 0.2–0.3): Show top 3 suggestions + ask for clarification
2. **Level 0** (score < 0.2): Show advisor contact directly

### R7 — Human Handover Must Be Available on Every Fallback
Every fallback screen must include a visible "Talk to Advisor" option with a real email or link.

---

## Multichannel Rules

### R8 — All 3 Channels Must Use Same core_bot.py
```python
# web_app.py, cli_app.py, whatsapp_mock.py all import:
from core_bot import chat
```

### R9 — CLI Channel Must Work Without Streamlit
`cli_app.py` must run with just `python cli_app.py` — no Streamlit dependency.

### R10 — WhatsApp Mock Must Simulate Message Format
WhatsApp mock output should simulate the message structure:
```
[WhatsApp Incoming] Student: When is the SEM 5 exam?
[WhatsApp Outgoing] Bot: The SEM 5 exams start on March 15th.
```

---

## Analytics Rules

### R11 — Report Must Propose Actionable Improvements
The Week 10 analysis must result in a written output (printed or in UI) that proposes at least:
- 5 new FAQ questions to add
- 2 intents to improve
- 1 pattern observed in student queries

### R12 — Analytics Dashboard Must Have at Least 3 Charts
Minimum: total queries over time, intent distribution, fallback rate.

---

## Submission Rules

### R13 — Project Must Run from Fresh Install
Test: create a new virtual environment, run `pip install -r requirements.txt`, then `streamlit run app.py`. It must work.

### R14 — README Must Be Complete
The final README must include: project overview, setup steps, how to run each channel, and a screenshot of the Streamlit app.
