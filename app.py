"""
Streamlit chat UI for the agent (memory + tools).
Run: streamlit run app.py
"""

import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

from src.agent import build_agent_executor, run_agent

load_dotenv()

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Chatbot with Memory & Tools", page_icon="🤖", layout="centered")
st.title("🤖 Chatbot with Memory & Tools")
st.caption("Multi-turn chat with search, calculator, and API tools. Conversation is remembered.")

# ---------------------------------------------------------------------------
# Session state: chat history and agent
# ---------------------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# StreamlitChatMessageHistory persists messages to session_state
history = StreamlitChatMessageHistory(key="chat_history")

# Lazy-build agent executor with this history (once per session)
if "agent_executor" not in st.session_state:
    try:
        st.session_state.agent_executor = build_agent_executor(chat_history=history)
    except ValueError as e:
        st.session_state.agent_executor = None
        st.session_state.agent_error = str(e)

# ---------------------------------------------------------------------------
# Sidebar: clear chat
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("### Tools")
    st.markdown("- **Search** — web search")
    st.markdown("- **Calculator** — math expressions")
    st.markdown("- **API** — weather, quotes")
    st.markdown("---")
    if st.button("Clear chat"):
        history.clear()
        st.session_state.messages = []
        # Rebuild executor with fresh history
        try:
            st.session_state.agent_executor = build_agent_executor(chat_history=history)
        except ValueError:
            pass
        st.rerun()

# ---------------------------------------------------------------------------
# Show agent error if no API key
# ---------------------------------------------------------------------------

if st.session_state.get("agent_error"):
    st.error(st.session_state.agent_error)
    st.info("Create a `.env` file with `GOOGLE_API_KEY=your-key` (get a free key at https://aistudio.google.com/apikey). See `.env.example`.")
    st.stop()

# ---------------------------------------------------------------------------
# Render existing messages
# ---------------------------------------------------------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------------------------------------------
# Chat input and run agent
# ---------------------------------------------------------------------------

if prompt := st.chat_input("Ask anything (e.g. 'What is 25 * 4?' or 'Search for latest AI news')"):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                response = run_agent(st.session_state.agent_executor, prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"})
