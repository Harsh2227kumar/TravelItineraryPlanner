# ⏭️ Next Steps — Weeks 1–4: Core FAQ Chatbot

## After Week 1 (Basic FAQ Responder)
- [ ] Your bot answers 10–15 hardcoded questions via if-else
- [ ] It runs in CLI and basic Streamlit UI
- **Next:** Add preprocessing so messy student inputs still get matched (→ Week 2)

## After Week 2 (Preprocessing)
- [ ] Inputs are cleaned: lowercase, no stopwords, no punctuation, spelling fixed
- [ ] Same question phrased differently still returns the correct answer
- **Next:** Handle synonyms — "fees" vs "tuition" vs "payment" should all work (→ Week 3)

## After Week 3 (Synonym-Aware Bot)
- [ ] Synonym dictionary built and mapped to canonical keywords
- [ ] Bot handles varied vocabulary from students
- **Next:** Move beyond exact matching — use TF-IDF similarity scoring (→ Week 4)

## After Week 4 (TF-IDF Retrieval)
- [ ] Bot uses cosine similarity to find best FAQ match
- [ ] No more fragile if-else — any similar question gets a relevant answer
- **Next (Week 5–7 phase):** Teach the bot to understand *intent* — what kind of question is being asked?

---

## Checklist Before Moving to Weeks 5–7

- [ ] `faqs.json` has at least 15 well-written Q&A pairs
- [ ] Preprocessing pipeline is a reusable function (not copy-pasted code)
- [ ] TF-IDF bot returns a confidence score with each answer
- [ ] Streamlit UI shows: input box, bot response, confidence score
- [ ] Code is clean, commented, and organized in `weeks/` folder

---

## Known Limitations to Fix Later
| Limitation | Fixed In |
|-----------|---------|
| Bot doesn't know *what type* of question is asked | Week 5 |
| Can't extract course codes or dates from queries | Week 6 |
| No memory between messages | Week 7 |
| No fallback when bot doesn't know the answer | Week 8 |
