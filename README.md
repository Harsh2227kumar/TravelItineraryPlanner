# 🎓 College FAQ Chatbot (Production-Ready)

An intelligent, scalable FAQ chatbot for college students. This repository has been upgraded from a prototype to a full production microservices architecture featuring a **FastAPI** backend and a **Streamlit** frontend, orchestrated via **Docker**.

---

## 🏗️ Architecture

```
college-chatbot/
│
├── docker-compose.yml          ← Production orchestration
├── backend.Dockerfile          ← FastAPI Server container
├── frontend.Dockerfile         ← Streamlit UI container
│
├── src/
│   ├── api/                    ← ✨ NEW: FastAPI Backend
│   │   ├── main.py             ← API routes (/chat, /analytics)
│   │   └── schemas.py          ← Pydantic validation models
│   │
│   ├── core/                   ← Core ML Intelligence
│   │   ├── intent.py           ← Intent Classification (LinearSVC)
│   │   ├── retrieval.py        ← Semantic Search (TF-IDF)
│   │   ├── entities.py         ← NER (spaCy)
│   │   ├── fallback.py         ← Soft & Hard Confidence Fallbacks
│   │   └── analytics.py        ← Interaction logger
│   │
│   └── ui/                     ← Frontend components
│
├── app.py                      ← ✨ UPDATED: Streamlit Client UI 
├── analytics/dashboard.py      ← ✨ UPDATED: Streamlit Analytics UI
│
└── data/                       
    ├── faqs.json               ← Knowledge base
    ├── intents.json            ← ML Training definitions
    └── logs/interactions.db    ← SQLite usage logs
```

---

## 🚀 Quick Start (Production via Docker)

The easiest and most scalable way to run the application is via Docker Compose.

```bash
# 1. Clone the repository
git clone <repo-url>
cd college-chatbot

# 2. Start the microservices
docker-compose up --build
```
*   **Frontend UI:** `http://localhost:8501`
*   **Backend API Docs (Swagger):** `http://localhost:8000/docs`

---

## 💻 Local Development Setup (Without Docker)

If you wish to run the backend and frontend separately on your host machine for debugging:

### 1. Backend Server (FastAPI)
```bash
# Create venv & install
python -m venv venv
venv\Scripts\activate            # Windows
source venv/bin/activate         # Mac/Linux
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Start API
uvicorn src.api.main:app --reload --port 8000
```

### 2. Frontend Server (Streamlit)
*In a new terminal window:*
```bash
venv\Scripts\activate
streamlit run app.py
```

---

## Running Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

All 42 tests should pass.

---

## Run Weekly Standalone Scripts

You can run each assignment week independently:

```bash
python weeks/week1_basic_bot.py
python weeks/week2_preprocessing.py
python weeks/week3_synonym_bot.py
python weeks/week4_tfidf_bot.py
python weeks/week5_intent_classifier.py
python weeks/week6_entity_extractor.py
python weeks/week7_context_handler.py
python weeks/week8_fallback_handler.py
python weeks/week9_multichannel_bot.py
python weeks/week10_analytics_reporter.py
```

---

## Features by Week

| Week | Feature | Key File |
|------|---------|----------|
| 1 | Basic FAQ Responder | `matcher.py` |
| 2 | Text Preprocessing | `preprocessor.py` |
| 3 | Synonym Expansion | `synonyms.py` |
| 4 | TF-IDF Retrieval | `retrieval.py` |
| 5 | Intent Classification (LinearSVC) | `intent.py` |
| 6 | Entity Extraction (spaCy) | `entities.py` |
| 7 | Multi-turn Context | `context.py` |
| 8 | Fallback & Advisor Handover | `fallback.py` |
| 9 | Multichannel Deployment | `core_bot.py` + `channels/` |
| 10 | Analytics Dashboard | `analytics.py` + `dashboard.py` |

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.9+ | Core language |
| Streamlit | Web UI & analytics dashboard |
| NLTK | Text preprocessing & stopwords |
| scikit-learn | TF-IDF vectorizer, LinearSVC classifier |
| spaCy | Named entity recognition |
| pandas | Data analysis & analytics |
| SQLite | Interaction logging |
| joblib | Model serialization |

---

## License

MIT
