"""Unit tests for quality and anomaly detection."""
from app.services.nlp.anomaly_detector import QualityAnomalyDetector
from app.services.extractors.base_extractor import ExtractionResult

def test_empty_document_anomaly():
    detector = QualityAnomalyDetector()
    dummy_extraction = ExtractionResult(
        file_type="txt", raw_text="", page_count=0, word_count=0,
        character_count=0, line_count=0, table_count=0
    )
    anomalies = detector.analyze(None, dummy_extraction, "")
    assert len(anomalies) > 0
    assert anomalies[0]["type"] == "EMPTY_DOCUMENT"
    assert anomalies[0]["severity"] == "HIGH"
