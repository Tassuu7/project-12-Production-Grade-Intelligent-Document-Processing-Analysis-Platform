"""Unit tests for keyword extraction."""
from app.services.nlp.keyword_extractor import KeywordExtractor

def test_keyword_extraction():
    text = "Intelligent document processing platforms leverage natural language processing and machine learning algorithms for automated extraction."
    extractor = KeywordExtractor()
    kws = extractor.extract(text, top_k=5)
    assert len(kws) > 0
    terms = [k["term"] for k in kws]
    assert any("document" in t or "processing" in t or "learning" in t for t in terms)
