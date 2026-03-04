# 🚀 Getting Started — Weeks 1–4: Core FAQ Chatbot

## What You're Building
A rule-based to retrieval-based college FAQ chatbot that answers questions about timings, fees, exams, contacts, and more — progressively smarter each week.

---

## Tech Stack
| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| Streamlit | Web UI |
| NLTK | Text preprocessing, tokenization |
| scikit-learn | TF-IDF vectorizer |
| pandas | FAQ data management |

---

## Folder Structure
```
college-chatbot/
│
├── data/
│   └── faqs.json            # Your FAQ database
│
├── weeks/
│   ├── week1_basic_bot.py
│   ├── week2_preprocessing.py
│   ├── week3_synonym_bot.py
│   └── week4_tfidf_bot.py
│
├── app.py                   # Streamlit UI (integrates all weeks)
├── requirements.txt
└── README.md
```

---

## Installation

```bash
# 1. Clone or create your project folder
mkdir college-chatbot && cd college-chatbot

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install streamlit nltk scikit-learn pandas

# 4. Download NLTK data
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

# 5. Run the app
streamlit run app.py
```

---

## Week-by-Week Kickoff

### Week 1 — Basic FAQ Responder
- Create `faqs.json` with 10–15 Q&A pairs (fees, timings, contacts, etc.)
- Build if-else or pattern matching logic to return answers
- Run as a simple CLI first, then plug into Streamlit

### Week 2 — Preprocessing Student Queries
- Apply lowercase, tokenization, stopword removal, punctuation cleanup
- Add basic spelling normalization
- Test: same question asked differently should still get matched

### Week 3 — Synonym-Aware FAQ Bot
- Build a synonym dictionary (e.g., "fees" → "tuition", "payment")
- Map all synonyms to canonical keywords before matching

### Week 4 — FAQ Retrieval with TF-IDF
- Store FAQs in a corpus
- Use `TfidfVectorizer` + cosine similarity to find best matching answer
- Replace hard-coded matching with similarity scores

---

## Running Each Week Independently
```bash
python weeks/week1_basic_bot.py
python weeks/week2_preprocessing.py
# etc.
```

---

## First Thing To Do Right Now
1. Create the folder structure above
2. Write your `faqs.json` with real institute data
3. Start `week1_basic_bot.py`
