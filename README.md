# SkAi Ultimate Master API

A multi-engine FastAPI backend that analyzes user questions, detects language automatically, searches the web, and composes structured answers—without requiring a Gemini API key.

## Key Features
- **Question & Intent Analysis:** Detects request type (`concept_explanation`, `code_generation`, `calculation_or_formula`, `comparison`, `emotional_support`), tone, and key terms.
- **Multilingual Understanding & Reply:** Automatically detects user language/script (Hindi, Hinglish, English, Marathi, and more) and replies in the same language.
- **Smart Thinking & Answer Composer:** Builds a step-by-step `thinking_process` and formats `final_answer` cleanly without external LLM keys.
- **Modular Routing:** Routes queries to dedicated logic engines (`math_logic.py`, `python_logic.py`, `javascript_logic.py`, `programming_engine.py`) with web search fallback.

## Project Files
- `main.py` — FastAPI app, analyzer, language detector, search handler, and answer composer.
- `requirements.txt` — Python dependencies for local setup and Render deployment.
- `math_logic.py`, `python_logic.py`, `javascript_logic.py`, `programming_engine.py` — Local logic engines.

## Endpoints
- `GET /` — Health and status check.
- `POST /fetch-info` — Accepts `query`, `language`, `reply_language`, `response_style`, `force_google`, and `show_thinking`.

## Run Locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload
