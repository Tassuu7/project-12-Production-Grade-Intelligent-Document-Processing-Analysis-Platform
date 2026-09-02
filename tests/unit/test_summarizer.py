"""Unit tests for extractive summarization."""
from app.services.nlp.summarizer import ExtractiveSummarizer

def test_extractive_summarization():
    text = (
        "Enterprise document systems automate high volume unstructured content ingestion. "
        "Local machine learning provides high data sovereignty and eliminates external cloud API dependencies. "
        "Extractive summarization captures the most informative sentences using graph centrality. "
        "Businesses reduce manual processing costs while enhancing analytical throughput."
    )
    summarizer = ExtractiveSummarizer()
    res = summarizer.summarize(text, sentence_count=2)
    assert "summary" in res
    assert len(res["sentences"]) == 2
    assert len(res["key_points"]) > 0
