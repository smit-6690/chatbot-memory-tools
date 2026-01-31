"""LangChain agent with memory and tools (search, calculator, custom API). Uses LCEL + tool binding (no deprecated agents)."""

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

from src.tools import search_tool, calculator_tool, custom_api_tool

# ---------------------------------------------------------------------------
# Tools and LLM
# ---------------------------------------------------------------------------

TOOLS = [search_tool, calculator_tool, custom_api_tool]
TOOLS_BY_NAME = {t.name: t for t in TOOLS}

SYSTEM_PROMPT = """You are a helpful assistant with access to tools. Use them when they would help answer the user.

Available tools:
- search_tool: for current information, news, or facts (input: search query)
- calculator_tool: for math (input: expression like "2 + 3" or "10 * 5")
- custom_api_tool: for weather (action="weather", param=city) or quotes (action="quote", param=optional topic)

Answer in a clear, concise way. If you use a tool, summarize the result for the user. Remember the conversation context."""


def get_llm():
    """Create Gemini chat model."""
    api_key = (os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or "").strip()
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")
    return ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        temperature=0,
        api_key=api_key,
    )


# ---------------------------------------------------------------------------
# Agent loop (LCEL + tool binding, no create_react_agent / AgentExecutor)
# ---------------------------------------------------------------------------

def _content_to_str(content) -> str:
    """Normalize message content to string (Gemini/LangChain can return a list of parts)."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for c in content:
            if isinstance(c, dict):
                parts.append(c.get("text", c.get("content", "")))
            else:
                parts.append(str(c))
        return " ".join(parts).strip()
    return str(content).strip()


def _run_tools(tool_calls, messages):
    """Run tool calls and return new messages to append."""
    new_messages = []
    for tc in tool_calls:
        name = tc.get("name", "")
        args = tc.get("args") or {}
        tool_call_id = tc.get("id", "")
        tool = TOOLS_BY_NAME.get(name)
        if tool:
            try:
                result = tool.invoke(args)
            except Exception as e:
                result = f"Error: {str(e)}"
        else:
            result = f"Unknown tool: {name}"
        new_messages.append(ToolMessage(content=str(result), tool_call_id=tool_call_id))
    return new_messages


def build_agent_executor(chat_history=None):
    """Build an executor object that holds LLM, tools, and chat history. No deprecated agents."""
    llm = get_llm()
    return {
        "llm": llm,
        "tools": TOOLS,
        "chat_history": chat_history,
    }


def run_agent(executor, user_message: str) -> str:
    """Run the agent with the given user message; return assistant reply. Uses LCEL + tool binding."""
    llm = executor["llm"]
    chat_history = executor.get("chat_history")

    # Build message list: system + history + current user
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    if chat_history and hasattr(chat_history, "messages"):
        messages.extend(list(chat_history.messages))
    messages.append(HumanMessage(content=user_message))

    # Persist user message to history
    if chat_history:
        chat_history.add_user_message(user_message)

    llm_with_tools = llm.bind_tools(TOOLS)
    max_iterations = 5
    final_content = ""

    for _ in range(max_iterations):
        response = llm_with_tools.invoke(messages)
        final_content = _content_to_str(response.content)

        if not getattr(response, "tool_calls", None):
            break

        messages.append(AIMessage(content=response.content or "", tool_calls=response.tool_calls))
        messages.extend(_run_tools(response.tool_calls, messages))

    # Persist assistant reply to history
    if chat_history and final_content:
        chat_history.add_ai_message(final_content)

    return (final_content or "I didn't get a response.").strip()
