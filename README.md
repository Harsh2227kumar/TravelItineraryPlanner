# Hackoweek Portfolio & College FAQ Chatbot

This repository is a complete learning-to-production journey:
- a production-ready **College FAQ Chatbot** (FastAPI + Streamlit + Docker), and
- structured weekly/monthly deliverables (NLP progression + embedded/IoT mini-projects).

The flagship implementation lives in `college-chatbot/` and includes a full API backend, web chat UI, analytics dashboard, training pipeline, tests, and containerized deployment.

---

## 1) Project Overview

### What this project does
The chatbot answers student questions about common college topics (fees, admissions, timings, etc.) using a layered NLP pipeline:
1. text preprocessing,
2. intent classification,
3. semantic FAQ retrieval,
4. entity extraction,
5. context-aware response handling,
6. confidence-based fallback + advisor handover,
7. analytics logging and dashboarding.

### Why this project matters
- Demonstrates end-to-end AI product development from prototype to deployable service.
- Separates concerns with a clean microservice architecture.
- Tracks performance with interaction analytics for iterative improvement.
- Keeps a strong educational traceability through week-by-week artifacts.

---

## 2) Repository Map

```text
Hackoweek/
├── README.md                          # You are here (root overview)
├── college-chatbot/                   # Main production project
│   ├── app.py                         # Streamlit chat UI client
│   ├── analytics/dashboard.py         # Streamlit analytics dashboard
│   ├── src/api/main.py                # FastAPI endpoints (/chat, /analytics/*)
│   ├── src/core/                      # NLP, fallback, analytics, context logic
│   ├── data/                          # FAQs, intents, SQLite logs
│   ├── models/                        # Serialized trained model artifacts
│   ├── tests/                         # Automated tests for core modules
│   ├── backend.Dockerfile             # Backend container definition
│   ├── frontend.Dockerfile            # Frontend container definition
│   ├── docker-compose.yml             # 2-service orchestration
│   └── train.py                       # Intent classifier training script
├── month-1/ ... month-3/              # Design/CRD/rules/quick-reference docs
└── month-4/week-11..15/               # Embedded systems mini-projects (.ino)
```

---

## 3) Core Architecture (College Chatbot)

### Runtime services
- **Backend**: FastAPI service on port `8000`
    - `/chat` for response generation
    - `/analytics/summary`, `/analytics/logs`, `/analytics/unhandled`
    - `/health` for service readiness checks
- **Frontend**: Streamlit service on port `8501`
    - chat interface (`app.py`)
    - analytics dashboard (`analytics/dashboard.py`)

### Processing pipeline
1. User query received (Web/API/Channel)
2. Preprocessing + feature preparation
3. Intent prediction (scikit-learn LinearSVC pipeline)
4. FAQ retrieval via TF-IDF similarity
5. Entity extraction (spaCy)
6. Fallback policy
     - `answer`
     - `fallback_soft` (clarification + suggestions)
     - `fallback_hard` (handover contact)
7. Interaction logging to SQLite
8. Dashboard aggregates usage and confidence trends

### Design goals
- Modularity (`src/core`, `src/api`, `src/ui` separation)
- Channel-agnostic bot logic (`core_bot.py`)
- Production portability (Docker + environment-driven endpoint URLs)

---

## 4) Tech Stack

| Layer | Tools |
|------|------|
| Language | Python 3.9+ |
| API | FastAPI, Uvicorn, Pydantic |
| UI | Streamlit |
| NLP/ML | NLTK, scikit-learn, spaCy |
| Data & Analytics | pandas, SQLite |
| Serialization | joblib |
| Visualization | Plotly, Streamlit charts |
| Packaging/Deploy | Docker, Docker Compose |

---

## 5) Prerequisites

For local development:
- Python 3.9+
- pip
- (Recommended) virtual environment
- spaCy English model: `en_core_web_sm`

For containerized deployment:
- Docker
- Docker Compose

---

## 6) Quick Start (Docker - Recommended)

From the project root:

```bash
cd college-chatbot
docker-compose up --build
```

Access:
- Chat UI: `http://localhost:8501`
- API docs (Swagger): `http://localhost:8000/docs`
- Health endpoint: `http://localhost:8000/health`

Notes:
- `data/` and `models/` are mounted as volumes for persistence.
- Frontend uses `API_URL=http://backend:8000` inside Docker network.

---

## 7) Local Development Setup (Without Docker)

Run from `college-chatbot/`.

### Step 1: Install dependencies

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Step 2: Start backend API

```bash
uvicorn src.api.main:app --reload --port 8000
```

### Step 3: Start chat UI (new terminal)

```bash
venv\Scripts\activate
streamlit run app.py
```

### Step 4: Start analytics dashboard (optional, new terminal)

```bash
venv\Scripts\activate
streamlit run analytics/dashboard.py
```

---

## 8) API Usage

### POST `/chat`
Request:

```json
{
    "query": "What is the hostel fee?",
    "channel": "web"
}
```

Response types:
- `answer`: confident direct answer with score
- `fallback_soft`: clarification + top suggestions
- `fallback_hard`: unable to answer; advisor handover message

Example curl:

```bash
curl -X POST "http://localhost:8000/chat" \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"What is admission deadline?\",\"channel\":\"web\"}"
```

### GET `/analytics/summary`
Returns high-level metrics:
- total queries
- average confidence
- fallback rate
- top intents

### GET `/analytics/logs`
Returns raw interaction logs suitable for table display/export.

### GET `/analytics/unhandled`
Returns most frequent fallback queries for FAQ expansion planning.

---

## 9) Training & Models

Train/refresh the intent classifier:

```bash
python train.py
```

Training script:
- runs classifier training,
- prints accuracy and classification report,
- signals readiness at 85%+ accuracy threshold.

Model artifacts are stored under `models/`.

---

## 10) Testing

Run all tests:

```bash
python -m pytest tests/ -v
```

Test coverage focuses on:
- intent classification
- retrieval behavior
- entity extraction
- fallback handling
- analytics helpers

---

## 11) Weekly Progression (NLP Track)

| Week | Capability | Representative Files |
|------|------------|----------------------|
| 1 | Basic matcher chatbot | `utils/matcher.py`, `weeks/week1_basic_bot.py` |
| 2 | Text preprocessing | `src/core/preprocessor.py`, `weeks/week2_preprocessing.py` |
| 3 | Synonym expansion | `src/core/synonyms.py`, `weeks/week3_synonym_bot.py` |
| 4 | TF-IDF retrieval | `src/core/retrieval.py`, `weeks/week4_tfidf_bot.py` |
| 5 | Intent classifier | `src/core/intent.py`, `weeks/week5_intent_classifier.py` |
| 6 | Entity extraction | `src/core/entities.py`, `weeks/week6_entity_extractor.py` |
| 7 | Multi-turn context | `src/core/context.py`, `weeks/week7_context_handler.py` |
| 8 | Fallback + handover | `src/core/fallback.py`, `weeks/week8_fallback_handler.py` |
| 9 | Multichannel architecture | `core_bot.py`, `channels/`, `weeks/week9_multichannel_bot.py` |
| 10 | Analytics dashboard | `src/core/analytics.py`, `analytics/dashboard.py` |

---

## 12) Month 4 Embedded/IoT Track

Additional practical hardware mini-projects:
- Week 11: Smart Door (`month-4/week-11/smart_door`)
- Week 12: Forklift Safety (`month-4/week-12/forklift_safety`)
- Week 13: Vending Machine (`month-4/week-13/vending_machine`)
- Week 14: Assembly Counter (`month-4/week-14/assembly_counter`)
- Week 15: Parking Slot (`month-4/week-15/parking_slot`)

Each folder includes Arduino sketch (`.ino`) and README.

---

## 13) Data & Persistence

- FAQ knowledge base: `college-chatbot/data/faqs.json`
- Intent training data: `college-chatbot/data/intents.json`
- Interaction database: `college-chatbot/data/logs/interactions.db`
- Trained models: `college-chatbot/models/`

Back up the `data/` and `models/` directories for durable deployments.

---

## 14) Troubleshooting

- Backend not reachable from UI:
    - ensure API is running on port `8000`
    - verify `API_URL` environment variable
- spaCy errors:
    - run `python -m spacy download en_core_web_sm`
- Empty dashboard:
    - interact with chatbot first to generate logs
- Docker startup issues:
    - run `docker-compose down` then `docker-compose up --build`

---

## 15) Roadmap

Planned improvements:
- stronger intent training data and class balancing
- richer entity support (program, campus, fee category)
- authentication and role-aware analytics
- CI pipeline for automated tests/build
- cloud deployment templates (Azure/AWS/GCP)

---

## 16) Contribution Guidelines

1. Create a feature branch
2. Keep changes modular and tested
3. Run `python -m pytest tests/ -v`
4. Update docs for behavioral/API changes
5. Open a pull request with a concise summary

---

## 17) License

MIT
