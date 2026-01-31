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

## Publish to GitHub

**If `git` is not recognized:** Install Git from [git-scm.com/download/win](https://git-scm.com/download/win) (Windows). Restart the terminal after installing.

1. Create a new repo at [github.com/new](https://github.com/new) (e.g. `chatbot-memory-tools`). Do **not** add README, .gitignore, or license.
2. In this project folder:

   ```bash
   git init
   git add .
   git commit -m "Initial commit: Chatbot with memory and tools"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/chatbot-memory-tools.git
   git push -u origin main
   ```

   Replace `YOUR_USERNAME` and `chatbot-memory-tools` with your GitHub username and repo name.  
   `.env` is in `.gitignore`, so your API key is not pushed.

---

## Resume Bullets (Suggested)

- Built a multi-turn chatbot with LangChain and Google Gemini using LCEL, tool binding, and conversation memory; tools include web search (DuckDuckGo), calculator, and custom API (weather, quotes).
- Implemented agentic design with session-persistent chat history; served via Streamlit UI.
