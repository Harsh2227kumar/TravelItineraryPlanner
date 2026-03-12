# Project Status (Verified)

Last updated: 2026-03-12

This status reflects code + test verification against:
- month-1 (Weeks 1-4) detailed instructions
- month-2 (Weeks 5-7) detailed instructions
- Week 8-10 roadmap from the assignment plan

---

## 1) Current Execution Health

- ✅ Test suite: **42/42 passed** (`python -m pytest tests -q`)
- ⚠️ Intent training run: **77.7% CV accuracy** (`python train.py`)
- ✅ Core app structure is running in production style (FastAPI + Streamlit)

---

## 2) Week-by-Week Completion Status

| Week | Task | Status | Notes |
|------|------|--------|-------|
| 1 | Basic FAQ responder | ✅ Completed | Implemented via `src/core/matcher.py` + `data/faqs.json` |
| 2 | Preprocessing student queries | ✅ Completed | `src/core/preprocessor.py` (lowercase, punctuation, stopwords) |
| 3 | Synonym-aware FAQ bot | ✅ Completed | `src/core/synonyms.py` |
| 4 | FAQ retrieval with TF-IDF | ✅ Completed | `src/core/retrieval.py` returns answer + confidence |
| 5 | Intent classification | ⚠️ Partial | Implemented, but month-2 target not met (accuracy < 85%; intents count > 7) |
| 6 | Entity extraction | ✅ Completed | `src/core/entities.py` returns required dict structure |
| 7 | Context handling follow-ups | ⚠️ Partial | Module exists, but main production path does not fully apply context flow |
| 8 | Fallbacks and handover | ✅ Completed | `src/core/fallback.py` soft + hard fallback with advisor details |
| 9 | Multichannel deployment mockup | ⚠️ Partial | Channel-agnostic core exists and week demo works, but dedicated `channels/cli_app.py` and `channels/whatsapp_mock.py` are still missing |
| 10 | Analytics and improvement | ⚠️ Partial | Logging/dashboard exist; improvement workflow needs stronger formalization |

Estimated overall completion: **~84% fully compliant** with month-wise instruction rules.

---

## 3) Month-1 Compliance (Weeks 1-4)

### Completed
- FAQ JSON is used as data source (`data/faqs.json`)
- Minimum FAQ count exceeded (43)
- TF-IDF + confidence available
- Required modules are present and tested
- `weeks/` standalone scripts are now present and runnable (`weeks/week1_basic_bot.py` ... `weeks/week10_analytics_reporter.py`)

### Gaps
- ⚠️ Standalone scripts are available, but these are currently lightweight demos built on production modules (not separate week-only logic branches)

---

## 4) Month-2 Compliance (Weeks 5-7)

### Completed
- Intent classifier module, entity extractor, and context module are present
- `intents.json` has descriptions and sufficient examples per intent
- Entity extractor returns consistent keys (`dates`, `course_codes`, `semester`)

### Gaps
- ❌ Required intent count is 5-7; current file has 10 intents
- ❌ Required accuracy is >85%; current training output is 77.7%
- ⚠️ Main UI/API flow does not consistently expose/resolve context in the same way as month-2 spec

---

## 5) Highest-Priority Next Actions

1. Re-align intent set to 7 required intents (`fees`, `exams`, `timetable`, `hostel`, `scholarships`, `admissions`, `contact`)
2. Retrain + tune classifier until validation accuracy is >=85%
3. Add missing channel adapters for week-9 compliance (`channels/cli_app.py` and `channels/whatsapp_mock.py`)
4. Make main UI/API context behavior fully align with month-2 follow-up handling spec
5. Formalize week-10 improvement outputs (5 FAQ proposals + 2 intent improvements + 1 pattern summary)

---

## 6) Short Conclusion

The project is technically stable and test-clean, but still not fully aligned with month-wise academic compliance requirements. Core functionality is strong; compliance-focused restructuring is needed to mark all weeks as fully complete.

