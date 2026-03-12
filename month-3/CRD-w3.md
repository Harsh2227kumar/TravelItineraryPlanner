# 📄 CRD — Component Requirements Document: Weeks 8–10

## Project: College FAQ Chatbot — Phase 3 (Production Ready)

---

## Component 11: Fallback Handler
**File:** `utils/fallback.py`
**Introduced in:** Week 8

| Function | Input | Output |
|----------|-------|--------|
| `handle_response(query)` | Raw query | Response dict with type |
| `get_top_n_answers(query, n)` | Query + count | List of top N FAQ matches |

**Response dict structure:**
```python
# Answered
{"type": "answer", "answer": "...", "score": 0.72}

# Fallback Level 1 (score 0.2–0.3)
{"type": "fallback_soft", "suggestions": [...], "clarification": "..."}

# Fallback Level 0 (score < 0.2)
{"type": "fallback_hard", "message": "...", "advisor_link": "mailto:..."}
```

**Acceptance Criteria:**
- Threshold constant defined in `config.py`
- Level 1 fallback returns 3 FAQ suggestions
- Level 0 fallback always includes advisor contact
- Every response type is handled in the UI

---

## Component 12: Core Bot (Channel-Agnostic)
**File:** `core_bot.py`
**Introduced in:** Week 9

| Function | Input | Output |
|----------|-------|--------|
| `chat(user_input)` | Raw query string | Final response dict |

**Internal flow:**
```
user_input → preprocess → predict_intent → extract_entities
          → resolve_context → handle_response → log_interaction → return
```

**Acceptance Criteria:**
- No Streamlit imports in this file
- Callable from web, CLI, and WhatsApp mock identically
- Logs every interaction before returning

---

## Component 13: Channel Adapters
**Files:** `channels/web_app.py`, `channels/cli_app.py`, `channels/whatsapp_mock.py`
**Introduced in:** Week 9

| Channel | Input Method | Output Method |
|---------|-------------|---------------|
| Web | `st.text_input` | `st.write`, `st.warning` |
| CLI | `input()` | `print()` |
| WhatsApp mock | `input()` with prefix | `print()` with [WhatsApp] tags |

**Acceptance Criteria:**
- All 3 import only from `core_bot.py` — no direct bot logic
- CLI runs with `python channels/cli_app.py`
- WhatsApp mock formats messages to simulate WA message bubbles

---

## Component 14: Interaction Logger
**File:** `utils/logger.py`
**Introduced in:** Week 10

| Function | Input | Output |
|----------|-------|--------|
| `init_db()` | — | Creates `interactions.db` if not exists |
| `log_interaction(...)` | query, intent, confidence, answer, was_fallback | Writes row to DB |
| `get_logs_df()` | — | Pandas DataFrame of all logs |

**DB Schema:**
```sql
CREATE TABLE logs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp   TEXT,
    query       TEXT,
    intent      TEXT,
    confidence  REAL,
    answer      TEXT,
    was_fallback INTEGER   -- 0 or 1
)
```

**Acceptance Criteria:**
- DB auto-created on first run
- Every `chat()` call writes exactly one log row
- `get_logs_df()` returns a valid pandas DataFrame

---

## Component 15: Analytics Dashboard
**File:** `analytics/dashboard.py`
**Introduced in:** Week 10

| Chart | Description |
|-------|-------------|
| Queries over time | Line chart grouped by day |
| Intent distribution | Bar chart of all predicted intents |
| Fallback rate | Gauge or % metric card |
| Top unhandled queries | Table of low-confidence queries |

**Acceptance Criteria:**
- Runs with `streamlit run analytics/dashboard.py`
- Reads from real `interactions.db` data
- Includes actionable improvement proposals section

---

## Dependencies Summary (New in Phase 3)
```
sqlite3     # built-in Python
plotly      # for analytics charts
pandas      # already installed
```
