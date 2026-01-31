"""Web search tool using DuckDuckGo (no API key required)."""

import time
import urllib.parse
from langchain_core.tools import tool


def _run_search(query: str, max_results: int = 8) -> list:
    """Run DuckDuckGo text search; return list of result dicts or empty list."""
    from duckduckgo_search import DDGS
    with DDGS() as ddgs:
        return list(ddgs.text(query, max_results=max_results))


@tool
def search_tool(query: str) -> str:
    """Search the web for current information. Use this when you need up-to-date facts, news, or general knowledge. Input should be a clear search query."""
    query = (query or "").strip() or "news"
    # Retry once on failure (DuckDuckGo can be flaky or rate-limited)
    for attempt in range(2):
        try:
            results = _run_search(query, max_results=8)
            if results:
                lines = []
                for i, r in enumerate(results, 1):
                    title = r.get("title", "")
                    body = r.get("body", r.get("snippet", ""))
                    link = r.get("href", r.get("link", r.get("url", "")))
                    lines.append(f"{i}. {title}\n   {body}\n   URL: {link}")
                return "\n\n".join(lines)
        except Exception as e:
            if attempt == 1:
                encoded = urllib.parse.quote_plus(query)
                return (
                    f"Search could not be completed: {e}. "
                    f"You can search directly here: https://duckduckgo.com/?q={encoded}"
                )
            time.sleep(1)
            continue
    encoded = urllib.parse.quote_plus(query)
    return (
        "No results were returned for that query. "
        f"You can try searching directly: https://duckduckgo.com/?q={encoded}"
    )
