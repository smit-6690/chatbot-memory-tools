"""Custom API tool: example weather-like and generic GET API calls."""

from langchain_core.tools import tool
import requests


@tool
def custom_api_tool(action: str, param: str = "") -> str:
    """Call a custom API. Actions: 'weather' (param: city name) or 'quote' (param: optional topic). Use for weather info or inspirational quotes."""
    action = action.strip().lower()
    param = (param or "").strip()

    if action == "weather":
        return _fake_weather(param or "Unknown")
    if action in ("quote", "random"):
        return _fetch_quote(param)
    return f"Unknown action: {action}. Use 'weather' or 'quote'."


def _fake_weather(city: str) -> str:
    """Return mock weather for demo (no real API key). Replace with OpenWeatherMap etc. in production."""
    # Demo: deterministic "weather" based on city name hash
    temp = 15 + (hash(city) % 20)
    conditions = ["Sunny", "Partly cloudy", "Cloudy", "Rainy", "Clear"]
    condition = conditions[hash(city) % len(conditions)]
    return f"Weather in {city}: {condition}, {temp}°C (demo data)."


# Fallback quotes when the external API is unreachable (e.g. network/firewall)
_FALLBACK_QUOTES = [
    '"The only way to do great work is to love what you do." — Steve Jobs',
    '"Innovation distinguishes between a leader and a follower." — Steve Jobs',
    '"Stay hungry, stay foolish." — Steve Jobs',
    '"It does not matter how slowly you go as long as you do not stop." — Confucius',
    '"The future belongs to those who believe in the beauty of their dreams." — Eleanor Roosevelt',
]


def _fetch_quote(topic: str) -> str:
    """Fetch a random quote from a public API; use fallback if the API is unreachable."""
    try:
        url = "https://api.quotable.io/random"
        if topic:
            url = f"https://api.quotable.io/random?tags={topic}"
        resp = requests.get(url, timeout=8)
        resp.raise_for_status()
        data = resp.json()
        return f'"{data.get("content", "")}" — {data.get("author", "Unknown")}'
    except Exception:
        import random
        return random.choice(_FALLBACK_QUOTES)
