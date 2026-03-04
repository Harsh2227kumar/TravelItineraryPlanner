# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] — 2026-03-05

### Added
- Intent classification engine (`src/core/intent.py`) — MultinomialNB, 98% accuracy
- Entity extraction (`src/core/entities.py`) — spaCy dates + regex course codes/semesters
- Multi-turn context handling (`src/core/context.py`) — session_state, 3-turn history
- Text preprocessor (`src/core/preprocessor.py`) — lowercase, stopwords, punctuation
- Intent training data (`data/intents.json`) — 10 intents, 250 examples
- Training script (`train.py`)
- Chat history UI, intent badge, entities expander, clear context button
- Tests for intent data validation and entity extraction

### Changed
- Updated `faqs.json` with 43 real SIT Nagpur Q&A pairs
- Updated pipeline to: preprocess → classify intent → extract entities → match answer
- Sidebar now shows 10 supported intents with clear context button

## [1.0.0] — 2026-03-04

### Added
- FAQ data store with 18 Q&A pairs across 6 categories
- Keyword-matching engine (`src/core/matcher.py`)
- Streamlit web UI with sidebar and confidence badges
- Centralized configuration (`src/config.py`)
- Data loader with validation (`src/data/loader.py`)
- Unit tests for the matcher engine
