"""Unit tests for multi-format document extractors."""
import os
from app.services.extractors import (
    DocumentExtractorFactory,
    PDFDocumentExtractor,
    DOCXDocumentExtractor,
    TXTDocumentExtractor,
    CSVDocumentExtractor,
    XLSXDocumentExtractor
)

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "sample_documents")

def test_extractor_factory_resolution():
    assert isinstance(DocumentExtractorFactory.get_extractor("pdf"), PDFDocumentExtractor)
    assert isinstance(DocumentExtractorFactory.get_extractor("docx"), DOCXDocumentExtractor)
    assert isinstance(DocumentExtractorFactory.get_extractor("txt"), TXTDocumentExtractor)
    assert isinstance(DocumentExtractorFactory.get_extractor("csv"), CSVDocumentExtractor)
    assert isinstance(DocumentExtractorFactory.get_extractor("xlsx"), XLSXDocumentExtractor)

def test_pdf_extractor():
    pdf_path = os.path.join(SAMPLES_DIR, "invoice_sample.pdf")
    if os.path.exists(pdf_path):
        extractor = PDFDocumentExtractor()
        res = extractor.extract(pdf_path)
        assert res.file_type == "pdf"
        assert res.page_count >= 1
        assert "INVOICE" in res.raw_text or len(res.raw_text) > 0

def test_docx_extractor():
    docx_path = os.path.join(SAMPLES_DIR, "resume_sample.docx")
    if os.path.exists(docx_path):
        extractor = DOCXDocumentExtractor()
        res = extractor.extract(docx_path)
        assert res.file_type == "docx"
        assert "JANE DOE" in res.raw_text
        assert res.word_count > 50

def test_txt_extractor():
    txt_path = os.path.join(SAMPLES_DIR, "research_report.txt")
    if os.path.exists(txt_path):
        extractor = TXTDocumentExtractor()
        res = extractor.extract(txt_path)
        assert res.file_type == "txt"
        assert "RESEARCH REPORT" in res.raw_text
        assert res.word_count > 100

def test_csv_extractor():
    csv_path = os.path.join(SAMPLES_DIR, "financial_records.csv")
    if os.path.exists(csv_path):
        extractor = CSVDocumentExtractor()
        res = extractor.extract(csv_path)
        assert res.file_type == "csv"
        assert res.table_count == 1
        assert res.tabular_statistics is not None
        assert "Operating_Revenue" in res.raw_text

def test_xlsx_extractor():
    xlsx_path = os.path.join(SAMPLES_DIR, "inventory_data.xlsx")
    if os.path.exists(xlsx_path):
        extractor = XLSXDocumentExtractor()
        res = extractor.extract(xlsx_path)
        assert res.file_type == "xlsx"
        assert res.table_count >= 1
        assert res.word_count > 20
