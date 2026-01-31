# Chatbot with Memory & Tools

A multi-turn AI chatbot with **conversation memory** and **tool use**: web search, calculator, and custom API (weather, quotes). Built with LangChain, Google Gemini, and Streamlit. Suitable for portfolio and resume projects.

---

## Features

- **Multi-turn chat** — Remembers conversation context within the session.
- **Tools**
  - **Search** — Web search via DuckDuckGo (no API key).
  - **Calculator** — Safe math expressions (e.g. `2 + 3`, `10 * 5`).
  - **Custom API** — Weather (demo) and random quotes (quotable.io with fallback).
- **Agentic design** — LCEL + tool binding; the model decides when to call tools.

## Tech Stack

| Layer   | Technology                    |
|--------|-------------------------------|
| LLM    | Google Gemini (gemini-2.5-flash) |
| Agent  | LangChain (LCEL, tool binding)   |
| UI     | Streamlit                       |
| Python | 3.10+                           |

---

## Setup

1. **Clone and enter the project**
   ```bash
   cd path/to/New-1
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   - Copy `.env.example` to `.env`.
   - Set your **Google AI (Gemini) API key** in `.env`:
     ```
     GOOGLE_API_KEY=your-key-here
     ```
   - Get a free key: [Google AI Studio](https://aistudio.google.com/apikey).
   - Optional: `GEMINI_MODEL=gemini-2.5-flash` to use a different model.

---

## Run

```bash
python -m streamlit run app.py
```

Open the URL shown (e.g. http://localhost:8501).

### Troubleshooting

- **"API key not valid"** — Use a key from [Google AI Studio](https://aistudio.google.com/apikey) only (not Google Cloud Console). No spaces around `=` in `.env`.
- **"API key not valid" (404 NOT_FOUND)** — Default model is `gemini-2.5-flash`. See [Gemini models](https://ai.google.dev/gemini-api/docs/models).
- **429 RESOURCE_EXHAUSTED** — Free tier quota (e.g. 20 requests/day). Wait for reset or try another model in `.env`.

---

## Project Layout

```
├── app.py              # Streamlit chat UI
├── requirements.txt
├── .env.example
├── src/
│   ├── agent.py        # LangChain agent (LCEL + tools, chat history)
│   └── tools/
│       ├── search.py   # DuckDuckGo search
│       ├── calculator.py
│       └── custom_api.py  # Weather (demo) + quotes
└── README.md
```

---

## Example Prompts

- "What is 25 * 4?"
- "Search for latest AI news"
- "What's the weather in London?" (demo)
- "Give me a random quote"
- "My name is Alex" → "What's my name?" (tests memory)

---


