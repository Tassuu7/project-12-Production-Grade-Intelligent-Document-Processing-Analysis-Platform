"""
Search Match Snippet Highlighter.
Extracts context windows around query terms and wraps them in highlighted HTML tags.
"""
import re
from typing import List

class SearchHighlighter:
    """Generates highlighted HTML snippet previews for search results."""

    @staticmethod
    def highlight_snippet(text: str, query: str, window_chars: int = 240) -> str:
        if not text or not query:
            return text[:window_chars] + "..." if len(text) > window_chars else text

        query_terms = [re.escape(t) for t in query.split() if len(t) > 1]
        if not query_terms:
            return text[:window_chars] + "..." if len(text) > window_chars else text

        pattern = re.compile(r'(' + '|'.join(query_terms) + r')', re.IGNORECASE)
        match = pattern.search(text)

        if not match:
            return text[:window_chars] + "..." if len(text) > window_chars else text

        start_pos = max(0, match.start() - window_chars // 2)
        end_pos = min(len(text), match.end() + window_chars // 2)

        snippet = text[start_pos:end_pos]
        if start_pos > 0:
            snippet = "..." + snippet
        if end_pos < len(text):
            snippet = snippet + "..."

        highlighted = pattern.sub(r'<mark style="background: #fef08a; padding: 0.1rem 0.25rem; border-radius: 3px; font-weight: 700;"></mark>', snippet)
        return highlighted
