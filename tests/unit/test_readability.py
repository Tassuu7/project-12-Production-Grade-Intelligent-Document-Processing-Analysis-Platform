"""Unit tests for Readability Analyzer."""
from app.services.nlp.readability_analyzer import ReadabilityAnalyzer

def test_readability_analysis():
    text = "The system automatically processes documents and extracts relevant text. It is fast and efficient."
    analyzer = ReadabilityAnalyzer()
    res = analyzer.analyze(text)
    assert "flesch_reading_ease" in res
    assert "flesch_kincaid_grade" in res
    assert res["flesch_reading_ease"] > 0
