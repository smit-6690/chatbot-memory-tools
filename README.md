# Chatbot with Memory and Tools

Multi-turn chatbot with **conversation memory** and **tool use** (search, calculator, API calls). Built with LangChain and Streamlit for a resume/portfolio project.

## Features

- **Multi-turn chat** — Conversation context is kept (buffer or optional summary).
- **Tools**  
  - **Search** — Web search via DuckDuckGo (no API key).  
  - **Calculator** — Safe math expressions (e.g. `2 + 3`, `10 * 5`).  
  - **Custom API** — Weather (demo) and quotes (quotable.io).
- **Memory** — Last N turns in buffer; optional summarised memory for long chats.
- **Agentic design** — ReAct-style agent that decides when to call tools.

## Tech stack

- **LangChain** — Agent, tools, memory.
- **Google Gemini** — LLM (gemini-2.5-flash by default).
- **Streamlit** — Chat UI.
- **Python 3.10+**

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
   - **Where to get the API key:** Go to [Google AI Studio](https://aistudio.google.com/apikey), sign in with your Google account, click **Get API key** or **Create API key**, then copy the key into `.env`.
   - Optional: `GEMINI_MODEL=gemini-2.5-flash`.

## Run

From the project folder (with your venv activated if you use one):

```bash
python -m streamlit run app.py
```

If `streamlit` is on your PATH you can use `streamlit run app.py` instead.

Open the URL shown in the terminal (e.g. http://localhost:8501). Use the chat input to ask questions; the agent can search, calculate, and call the demo API.

### "API key not valid" (400 INVALID_ARGUMENT)

- Get the key from **Google AI Studio** only: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey) (not from Google Cloud Console).
- In `.env`, use `GOOGLE_API_KEY=your-key` with no spaces around `=`, and no quotes around the key.
- Make sure there are no extra spaces or line breaks in the key; the app trims whitespace automatically.
- You can use `GEMINI_API_KEY` instead of `GOOGLE_API_KEY` if you prefer.

## Project layout

```
├── app.py                 # Streamlit chat UI
├── requirements.txt
├── .env.example
├── src/
│   ├── agent.py           # LangChain agent (LCEL + tools, chat history)
│   └── tools/
│       ├── search.py      # DuckDuckGo search
│       ├── calculator.py  # Math expression eval
│       └── custom_api.py  # Weather (demo) + quotes API
└── README.md
```

## Example prompts

- "What is 25 * 4?"
- "Search for latest news on large language models"
- "What's the weather in London?" (demo data)
- "Give me an inspirational quote"
- "Remember my name is Alex" then "What's my name?" (tests memory)

## Publish to GitHub

**If `git` is not recognized:** Install Git from [https://git-scm.com/download/win](https://git-scm.com/download/win) (Windows). During setup, choose "Git from the command line and also from 3rd-party software" so it is added to PATH. Restart the terminal (or Cursor) after installing.

**Alternative (no Git installed):** Create a new repo on GitHub, then use **"uploading an existing file"** and drag your project folder contents (do **not** upload the `.env` file or `.venv` folder).

---

1. **Create a new repository on GitHub**
   - Go to [https://github.com/new](https://github.com/new).
   - Choose a name (e.g. `chatbot-memory-tools`), set visibility to **Public**, and do **not** add a README, .gitignore, or license (this project already has them).
   - Click **Create repository**.

2. **Push this project from your machine**
   In the project folder (`New-1`), run:

   ```bash
   git init
   git add .
   git commit -m "Initial commit: Chatbot with memory and tools"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/chatbot-memory-tools.git
   git push -u origin main
   ```

   Replace `YOUR_USERNAME` with your GitHub username and `chatbot-memory-tools` with your repo name if different.

   Your repo link will be: **https://github.com/YOUR_USERNAME/chatbot-memory-tools**

   (`.env` is in `.gitignore`, so your API key will not be pushed.)

## Resume bullets (suggested)

- Built a multi-turn chatbot with LangChain using ReAct-style agent, conversation memory (buffer/summary), and tool use (search, calculator, API).
- Implemented agentic design with web search (DuckDuckGo), safe calculator, and custom API tools; served via Streamlit UI with session-persistent memory.
