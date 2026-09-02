"""
In-Memory Fast Inverted Search Indexer.
"""
from collections import defaultdict
from typing import Dict, Set, List
from app.services.nlp.text_preprocessor import TextPreprocessor

class SearchIndexer:
    """Inverted index over document IDs and token sets."""

    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.index: Dict[str, Set[int]] = defaultdict(set)

    def index_document(self, document_id: int, text: str) -> None:
        tokens = self.preprocessor.tokenize_words(text, remove_stopwords=True)
        for t in set(tokens):
            self.index[t].add(document_id)

    def remove_document(self, document_id: int) -> None:
        for t in self.index:
            self.index[t].discard(document_id)

    def search_term(self, term: str) -> Set[int]:
        normalized = term.lower().strip()
        return self.index.get(normalized, set())
