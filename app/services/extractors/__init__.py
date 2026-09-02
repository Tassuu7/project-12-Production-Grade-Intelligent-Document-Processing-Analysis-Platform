"""Extractors package index."""
from app.services.extractors.base_extractor import (
    BaseDocumentExtractor,
    ExtractionResult,
    PageContent,
    TableData
)
from app.services.extractors.pdf_extractor import PDFDocumentExtractor
from app.services.extractors.docx_extractor import DOCXDocumentExtractor
from app.services.extractors.txt_extractor import TXTDocumentExtractor
from app.services.extractors.csv_extractor import CSVDocumentExtractor
from app.services.extractors.xlsx_extractor import XLSXDocumentExtractor
from app.services.extractors.extractor_factory import DocumentExtractorFactory

__all__ = [
    "BaseDocumentExtractor",
    "ExtractionResult",
    "PageContent",
    "TableData",
    "PDFDocumentExtractor",
    "DOCXDocumentExtractor",
    "TXTDocumentExtractor",
    "CSVDocumentExtractor",
    "XLSXDocumentExtractor",
    "DocumentExtractorFactory",
]
