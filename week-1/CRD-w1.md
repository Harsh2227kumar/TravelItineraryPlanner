# 📄 CRD — Component Requirements Document: Weeks 1–4

## Project: College FAQ Chatbot — Phase 1 (Core FAQ System)

---

## Component 1: FAQ Data Store
**File:** `data/faqs.json`

| Attribute | Detail |
|-----------|--------|
| Format | JSON array of objects |
| Min entries | 15 Q&A pairs |
| Required fields | `question` (string), `answer` (string) |
| Optional fields | `category` (string) — e.g., "fees", "exams" |
| Owned by | Developer (you) — fill with real institute data |

**Acceptance Criteria:**
- Contains at least 15 pairs covering: fees, timings, contacts, exams, admissions, hostel
- Questions written in natural student language
- No duplicate questions

---

## Component 2: Preprocessing Module
**File:** `utils/preprocess.py`
**Introduced in:** Week 2

| Function | Input | Output |
|----------|-------|--------|
| `preprocess(text)` | Raw query string | Cleaned, normalized string |

**Must do:**
- Lowercase conversion
- Punctuation removal
- Stopword removal (NLTK English stopwords)
- Basic spelling normalization (optional: `pyspellchecker`)

**Acceptance Criteria:**
- `preprocess("What ARE the FEE?!")` → `"fee"`
- `preprocess("When is the EXAM scheduled?")` → `"exam scheduled"`
- Function is importable from other modules

---

## Component 3: Synonym Dictionary
**File:** `utils/synonyms.py`
**Introduced in:** Week 3

| Function | Input | Output |
|----------|-------|--------|
| `apply_synonyms(text)` | Preprocessed query | Query with synonyms replaced |

**Must include synonym groups for:**
- fees / tuition / payment / cost / charges
- timetable / schedule / timing / slots
- exam / test / assessment / evaluation
- contact / office / reach / helpdesk

**Acceptance Criteria:**
- "tuition payment schedule" → canonical keywords matched to correct FAQ
- Dictionary has minimum 4 synonym groups

---

## Component 4: TF-IDF Retrieval Engine
**File:** `utils/retrieval.py`
**Introduced in:** Week 4

| Function | Input | Output |
|----------|-------|--------|
| `build_index(faqs)` | FAQ list | Fitted TF-IDF matrix |
| `get_answer(query)` | Raw query string | `(answer: str, score: float)` |

**Dependencies:** `sklearn.feature_extraction.text.TfidfVectorizer`, `cosine_similarity`

**Acceptance Criteria:**
- Returns best matching answer for any student query
- Includes a float confidence score between 0 and 1
- Uses preprocessing + synonym mapping before vectorizing

---

## Component 5: Streamlit Web UI
**File:** `app.py`

| UI Element | Description |
|------------|-------------|
| Title | "🎓 College FAQ Chatbot" |
| Text input | Student types question here |
| Answer display | Shows bot's response |
| Confidence badge | Shows score, color-coded (green > 0.5, yellow > 0.3, red < 0.3) |
| Sidebar | About section, week label |

**Acceptance Criteria:**
- Runs with `streamlit run app.py`
- Answer appears within 2 seconds
- Confidence score visible on every response

---

## Dependencies Summary
```
nltk
scikit-learn
streamlit
pandas
pyspellchecker   # optional, Week 2
```
