"""
Extractor Factory routing files to their corresponding format parsers.
"""
from typing import Dict, Type
from app.services.extractors.base_extractor import BaseDocumentExtractor
from app.services.extractors.pdf_extractor import PDFDocumentExtractor
from app.services.extractors.docx_extractor import DOCXDocumentExtractor
from app.services.extractors.txt_extractor import TXTDocumentExtractor
from app.services.extractors.csv_extractor import CSVDocumentExtractor
from app.services.extractors.xlsx_extractor import XLSXDocumentExtractor
from app.core.exceptions import ValidationException

class DocumentExtractorFactory:
    """Factory resolving document extractors based on file extension."""

    _extractors: Dict[str, Type[BaseDocumentExtractor]] = {
        "pdf": PDFDocumentExtractor,
        "docx": DOCXDocumentExtractor,
        "txt": TXTDocumentExtractor,
        "csv": CSVDocumentExtractor,
        "xlsx": XLSXDocumentExtractor,
    }

    @classmethod
    def get_extractor(cls, file_type: str) -> BaseDocumentExtractor:
        normalized_ext = file_type.lower().strip()
        extractor_class = cls._extractors.get(normalized_ext)
        if not extractor_class:
            raise ValidationException(f"No extractor registered for document type: '{file_type}'")
        return extractor_class()
