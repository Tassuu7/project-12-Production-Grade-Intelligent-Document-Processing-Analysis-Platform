"""
Text Preprocessor and Normalization Engine.
Performs Unicode NFKC normalization, regex tokenization, sentence splitting,
stopword stripping, n-gram extraction, and character/word statistics.
"""
import re
import unicodedata
from typing import List, Tuple, Dict, Set
from app.services.nlp.vocabulary import STOP_WORDS

class TextPreprocessor:
    """Modular text normalization, sentence segmentation, and tokenization layer."""

    def __init__(self, custom_stopwords: Set[str] = None):
        self.stopwords = custom_stopwords or STOP_WORDS

    def clean_text(self, text: str) -> str:
        """Normalize Unicode characters, collapse redundant whitespace and control chars."""
        if not text:
            return ""
        
        # Unicode normalization (NFKC)
        normalized = unicodedata.normalize("NFKC", text)
        
        # Standardize linebreaks
        normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
        
        # Collapse multiple empty lines
        normalized = re.sub(r'\n{3,}', '\n\n', normalized)
        
        # Clean inline multiple spaces
        lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in normalized.splitlines()]
        
        return "\n".join(lines).strip()

    def tokenize_words(self, text: str, remove_stopwords: bool = False, min_len: int = 2) -> List[str]:
        """Tokenize text into lowercase alphanumeric tokens."""
        cleaned = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+(?:-[a-z0-9]+)*\b', cleaned)
        
        filtered = []
        for t in tokens:
            if len(t) >= min_len and not t.isdigit():
                if remove_stopwords and t in self.stopwords:
                    continue
                filtered.append(t)
        return filtered

    def split_sentences(self, text: str) -> List[str]:
        """Resilient sentence boundary detection handling abbreviations and numbers."""
        if not text:
            return []
        
        protected = text
        abbrevs = ["Mr.", "Mrs.", "Ms.", "Dr.", "Prof.", "Sr.", "Jr.", "vs.", "e.g.", "i.e.", "U.S.", "Inc.", "Ltd.", "Co."]
        for i, ab in enumerate(abbrevs):
            protected = protected.replace(ab, f"__ABBR_{i}__")
        
        raw_sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9\"\'\(\[])|\n{2,}', protected)
        
        final_sentences: List[str] = []
        for s in raw_sentences:
            cleaned_s = s.strip()
            for i, ab in enumerate(abbrevs):
                cleaned_s = cleaned_s.replace(f"__ABBR_{i}__", ab)
            
            cleaned_s = re.sub(r'\s+', ' ', cleaned_s)
            if len(cleaned_s) > 10:
                final_sentences.append(cleaned_s)
                
        return final_sentences

    def generate_ngrams(self, tokens: List[str], n: int = 2) -> List[str]:
        """Generate contiguous n-grams from a list of tokens."""
        if len(tokens) < n:
            return []
        return [" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]

    def compute_lexical_statistics(self, text: str) -> Dict[str, float]:
        """Compute word lengths, vocabulary richness, and readability approximations."""
        tokens = self.tokenize_words(text)
        sentences = self.split_sentences(text)
        
        if not tokens:
            return {
                "word_count": 0,
                "sentence_count": 0,
                "unique_words": 0,
                "lexical_diversity": 0.0,
                "avg_word_length": 0.0,
                "avg_sentence_length": 0.0
            }
        
        unique_tokens = set(tokens)
        avg_word_len = sum(len(t) for t in tokens) / len(tokens)
        avg_sent_len = len(tokens) / max(1, len(sentences))
        lex_diversity = len(unique_tokens) / len(tokens)
        
        return {
            "word_count": float(len(tokens)),
            "sentence_count": float(len(sentences)),
            "unique_words": float(len(unique_tokens)),
            "lexical_diversity": round(lex_diversity, 4),
            "avg_word_length": round(avg_word_len, 2),
            "avg_sentence_length": round(avg_sent_len, 2)
        }
