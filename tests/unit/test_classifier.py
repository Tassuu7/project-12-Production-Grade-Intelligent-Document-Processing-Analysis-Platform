"""Unit tests for local ML document classification."""
from app.services.nlp.classifier import DocumentClassifier

def test_invoice_classification():
    text = "INVOICE #9812 Subtotal: $400.00 Tax amount: $40.00 Total amount due: $440.00 Remit payment to bank wire transfer."
    clf = DocumentClassifier()
    res = clf.classify(text, "invoice_9812.pdf")
    assert res["predicted_category"] == "Invoice"
    assert res["confidence"] >= 0.50

def test_resume_classification():
    text = "CURRICULUM VITAE Work Experience Senior Software Engineer Education Bachelor of Science in Computer Science Skills Python Java"
    clf = DocumentClassifier()
    res = clf.classify(text, "resume_john.docx")
    assert res["predicted_category"] == "Resume"
    assert res["confidence"] >= 0.50

def test_report_classification():
    text = "EXECUTIVE SUMMARY Annual Performance Analysis Report Findings Recommendations Table of Contents Appendix Milestones"
    clf = DocumentClassifier()
    res = clf.classify(text, "annual_report.txt")
    assert res["predicted_category"] == "Report"
