"""
Base Interface and Unified Data Models for Document Extractors.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class TableData(BaseModel):
    """Standardized matrix structure for extracted tables."""
    table_index: int
    headers: List[str] = Field(default_factory=list)
    rows: List[List[str]] = Field(default_factory=list)
    row_count: int = 0
    column_count: int = 0
    sheet_name: Optional[str] = None

class PageContent(BaseModel):
    """Extracted content and statistics for a single page/sheet/section."""
    page_number: int
    text: str
    word_count: int
    character_count: int
    tables: List[TableData] = Field(default_factory=list)

class ExtractionResult(BaseModel):
    """Unified document extraction schema for all file formats."""
    file_type: str
    raw_text: str
    page_count: int
    word_count: int
    character_count: int
    line_count: int
    table_count: int
    pages: List[PageContent] = Field(default_factory=list)
    tables: List[TableData] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    structural_headings: List[str] = Field(default_factory=list)
    tabular_statistics: Optional[Dict[str, Any]] = None

class BaseDocumentExtractor(ABC):
    """Abstract base class for all file format extractors."""

    @abstractmethod
    def extract(self, filepath: str) -> ExtractionResult:
        """Extract text, structure, tables, and metadata from target file."""
        pass
