# 📋 Rules — Weeks 1–4: Core FAQ Chatbot

## Code Rules

### R1 — One File Per Week
Each week must have its own standalone Python file in `weeks/`. Do not mix Week 1 and Week 4 logic in the same file.

### R2 — Preprocessing is Always Reusable
The preprocessing function built in Week 2 must be imported and reused in Weeks 3 and 4. Never copy-paste it. Put it in a shared `utils/preprocess.py`.

### R3 — FAQs Must Live in faqs.json
Never hardcode FAQ data inside Python files. All Q&A pairs must be in `data/faqs.json`. Python files only read from it.

### R4 — No Week Skipping
Each week builds on the previous. Do not jump to TF-IDF (Week 4) without having preprocessing (Week 2) working correctly.

### R5 — Confidence Score is Mandatory from Week 4
Every answer returned by the TF-IDF bot must include a confidence score. This will be used in Week 8 for fallback logic.

---

## Data Rules

### R6 — Minimum FAQ Count
- Week 1: Minimum 10 FAQs
- Week 4: Minimum 15 FAQs (add more as you go)

### R7 — FAQ Questions Must Be Natural Language
Write FAQ questions the way a student would actually ask them — not like database entries.
- ✅ "What is the last date to pay fees?"
- ❌ "fees_payment_deadline"

### R8 — Synonyms Must Be Documented
Every synonym group added in Week 3 must be listed in the synonym dictionary with a comment explaining why it's grouped.

---

## UI Rules (Streamlit)

### R9 — Always Show Confidence Score
The Streamlit UI must display the confidence score alongside every answer from Week 4 onwards.

### R10 — Input Must Be a Text Box, Not Buttons
Students type questions — don't replace the text input with preset option buttons.

---

## Submission Rules

### R11 — Each Week Must Work Standalone
Running `python weeks/weekN_*.py` must demonstrate that week's feature independently.

### R12 — Comments Required
Every function must have at least a one-line comment explaining what it does.

### R13 — requirements.txt Must Be Updated
After installing any new library, add it to `requirements.txt` immediately.
