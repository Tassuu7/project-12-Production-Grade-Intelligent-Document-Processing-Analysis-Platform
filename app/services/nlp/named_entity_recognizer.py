"""
Local Rule and Gazetteer-Based Named Entity Recognizer (NER).
"""
import re
from typing import List, Dict, Any

class NamedEntityRecognizer:
    PATTERNS = {
        "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b",
        "PHONE": r"\b(?:\+?1[-. ]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})\b",
        "CURRENCY": r"\$[0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?",
        "DATE_ISO": r"\b\d{4}-\d{2}-\d{2}\b",
        "INVOICE_ID": r"\b(?:INV|PO|BILL)[-_#]?[0-9A-Z]{4,12}\b"
    }

    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        entities: List[Dict[str, Any]] = []
        for entity_type, pattern_str in self.PATTERNS.items():
            pattern = re.compile(pattern_str, re.IGNORECASE)
            for match in pattern.finditer(text):
                entities.append({
                    "entity_type": entity_type,
                    "text": match.group(0),
                    "start": match.start(),
                    "end": match.end(),
                    "confidence": 0.95
                })
        return sorted(entities, key=lambda x: x["start"])
