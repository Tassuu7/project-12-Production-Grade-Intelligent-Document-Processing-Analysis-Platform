"""
Readability and Text Complexity Scoring Engine.
"""
import re
from typing import Dict, Any

class ReadabilityAnalyzer:
    def analyze(self, text: str) -> Dict[str, Any]:
        if not text or len(text.strip()) < 10:
            return {"reading_ease": 0.0, "grade_level": 0.0, "complexity": "N/A"}

        words = re.findall(r"\b[a-zA-Z]+\b", text)
        sentences = [s.strip() for s in re.split(r"[.!?]+", text) if len(s.strip()) > 3]

        total_words = len(words)
        total_sentences = max(1, len(sentences))
        total_syllables = sum(self._count_syllables(w) for w in words)

        if total_words == 0:
            return {"reading_ease": 0.0, "grade_level": 0.0, "complexity": "N/A"}

        words_per_sentence = total_words / total_sentences
        syllables_per_word = total_syllables / total_words

        reading_ease = 206.835 - (1.015 * words_per_sentence) - (84.6 * syllables_per_word)
        reading_ease = max(0.0, min(100.0, reading_ease))

        grade_level = (0.39 * words_per_sentence) + (11.8 * syllables_per_word) - 15.59
        grade_level = max(1.0, grade_level)

        return {
            "flesch_reading_ease": round(reading_ease, 2),
            "flesch_kincaid_grade": round(grade_level, 2),
            "words_per_sentence": round(words_per_sentence, 2)
        }

    def _count_syllables(self, word: str) -> int:
        w = word.lower()
        if len(w) <= 3:
            return 1
        matches = re.findall(r'[aeiouy]{1,2}', w)
        return max(1, len(matches))
