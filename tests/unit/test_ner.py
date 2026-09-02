"""Unit tests for Named Entity Recognizer."""
from app.services.nlp.named_entity_recognizer import NamedEntityRecognizer

def test_ner_extraction():
    text = "Please send payment of $5,000.00 to support@nexus.com regarding invoice INV-2026-9912 before 2026-10-15."
    ner = NamedEntityRecognizer()
    entities = ner.extract_entities(text)
    types = [e["entity_type"] for e in entities]
    assert "CURRENCY" in types
    assert "EMAIL" in types
    assert "INVOICE_ID" in types
