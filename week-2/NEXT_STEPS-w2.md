# ⏭️ Next Steps — Weeks 5–7: Smart Query Understanding

## After Week 5 (Intent Classification)
- [ ] Bot classifies queries into 5–7 intents with good accuracy
- [ ] Classifier is saved as `models/intent_model.pkl`
- [ ] Routing logic sends query to the right FAQ subset
- **Next:** Extract *specific details* from the query like course codes and dates (→ Week 6)

## After Week 6 (Entity Extraction)
- [ ] spaCy extracts dates, semester numbers, course codes from queries
- [ ] Responses are personalized: "The SEM 5 CS exam is on March 15th"
- **Next:** Handle follow-up questions that rely on what was asked before (→ Week 7)

## After Week 7 (Context Handling)
- [ ] Bot remembers last intent and entities across 2–3 turns
- [ ] Vague follow-ups like "What about third year?" are resolved correctly
- [ ] `st.session_state` stores conversation context in Streamlit
- **Next (Week 8–10 phase):** Handle cases where bot doesn't know the answer gracefully

---

## Checklist Before Moving to Weeks 8–10

- [ ] Intent classifier accuracy > 85% on test sentences
- [ ] Entity extractor correctly handles at least: dates, SEM numbers, course codes
- [ ] Context handling tested with at least 3 multi-turn conversation flows
- [ ] All logic is modular — intent, entity, context are separate functions/files
- [ ] Streamlit UI shows: detected intent tag + extracted entities alongside answer

---

## Known Limitations to Fix Later
| Limitation | Fixed In |
|-----------|---------|
| No graceful handling when bot is unsure | Week 8 |
| Only works on web (Streamlit) | Week 9 |
| No record of what students are actually asking | Week 10 |
