# 🎓 College FAQ Chatbot

An intelligent FAQ chatbot for college students — answers questions about fees, timings, exams, admissions, hostel, and more.

## Architecture

```
app.py                     ← Streamlit entry point (thin)
│
├── src/core/              ← Business logic engines
│   ├── __init__.py        ← Public API: get_answer()
│   └── matcher.py         ← Keyword-matching engine
│
├── src/data/              ← Data access layer
│   └── loader.py          ← Load & validate faqs.json
│
├── src/ui/                ← UI components
│   ├── components.py      ← Answer card, confidence badge
│   └── sidebar.py         ← Sidebar layout
│
├── src/config.py          ← Centralized settings
│
├── data/faqs.json         ← FAQ database
└── tests/                 ← Unit tests
```

## Quick Start

```bash
# Clone the repo
git clone <repo-url>
cd college-chatbot

# Create virtual environment
python -m venv venv
venv\Scripts\activate           # Windows
source venv/bin/activate        # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the web UI
streamlit run app.py
```

## Running Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| Streamlit | Web UI |
| NLTK | Text preprocessing (upcoming) |
| scikit-learn | TF-IDF vectorizer (upcoming) |
| pandas | Data management |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Add your code in the appropriate `src/` sub-package
4. Write tests in `tests/`
5. Update `CHANGELOG.md`
6. Open a pull request

## License

MIT
