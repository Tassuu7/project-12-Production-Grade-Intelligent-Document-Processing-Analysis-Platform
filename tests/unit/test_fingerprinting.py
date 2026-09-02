"""Unit tests for Document Fingerprinting."""
from app.services.nlp.document_fingerprinting import DocumentFingerprinter

def test_simhash_identical_documents():
    doc1 = "The quick brown fox jumps over the lazy dog."
    doc2 = "The quick brown fox jumps over the lazy dog."
    fingerprinter = DocumentFingerprinter()
    h1 = fingerprinter.compute_simhash(doc1)
    h2 = fingerprinter.compute_simhash(doc2)
    assert h1 == h2
    assert fingerprinter.simhash_distance(h1, h2) == 0
