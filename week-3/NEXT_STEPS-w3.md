# ⏭️ Next Steps — Weeks 8–10: Production Ready

## After Week 8 (Fallbacks and Handover)
- [ ] Bot detects low-confidence answers (score < threshold)
- [ ] On fallback: shows clarifying question + top 3 related FAQs
- [ ] "Talk to Advisor" button routes to human contact
- **Next:** Make the same chatbot logic work across web, CLI, and WhatsApp mock (→ Week 9)

## After Week 9 (Multichannel Deployment)
- [ ] Web channel: fully working Streamlit app
- [ ] CLI channel: `cli_app.py` simulates mobile/terminal interaction
- [ ] WhatsApp mock: `whatsapp_mock.py` shows message in/out flow
- [ ] Core chatbot logic is **channel-agnostic** (same functions, different I/O)
- **Next:** Log all interactions and use data to improve the bot (→ Week 10)

## After Week 10 (Analytics and Continuous Improvement)
- [ ] All interactions logged to SQLite with timestamp, intent, confidence, answer
- [ ] Analytics dashboard shows: top queries, weak intents, unanswered questions
- [ ] At least 5 new FAQs proposed based on logged data
- [ ] Project is fully complete and documented

---

## Final Project Checklist (Submission Ready)

- [ ] All 10 weeks implemented and working
- [ ] README.md is complete with setup instructions
- [ ] `requirements.txt` is up to date
- [ ] Streamlit app runs with `streamlit run app.py` from a fresh install
- [ ] Analytics dashboard accessible from the app sidebar
- [ ] Code is clean, commented, and organized
- [ ] All week files in `weeks/` folder work independently

---

## What You've Built (Full Picture)
```
Week 1  → Rule-based FAQ bot
Week 2  → Preprocessing pipeline
Week 3  → Synonym handling
Week 4  → TF-IDF retrieval
Week 5  → Intent classification
Week 6  → Entity extraction
Week 7  → Multi-turn context
Week 8  → Fallback & handover
Week 9  → Multichannel mockup
Week 10 → Analytics dashboard
```
**Result:** A complete, intelligent, production-mockup college chatbot system.
