"""Web search and browser interaction skill."""
import urllib.parse
import webbrowser
from typing import Optional

class WebSkill:
    """Handles web queries, YouTube, and website navigation."""

    @staticmethod
    def open_url(url: str) -> str:
        """Open web URL in default browser."""
        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"https://{url}"
        webbrowser.open(url)
        return f"Opening {url}"

    @staticmethod
    def search_google(query: str) -> str:
        """Search Google for query."""
        encoded = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={encoded}"
        webbrowser.open(url)
        return f"Searching Google for '{query}'"

    @staticmethod
    def search_youtube(query: str) -> str:
        """Search YouTube for query."""
        encoded = urllib.parse.quote_plus(query)
        url = f"https://www.youtube.com/results?search_query={encoded}"
        webbrowser.open(url)
        return f"Searching YouTube for '{query}'"
