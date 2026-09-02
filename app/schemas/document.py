"""Document schemas for upload, list, filters, and details."""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class DocumentResponse(BaseModel):
    id: int
    user_id: int
    title: str
    original_filename: str
    file_type: str
    mime_type: str
    file_size_bytes: int
    file_hash_sha256: str
    page_count: int
    word_count: int
    character_count: int
    status: str
    error_message: Optional[str] = None
    processing_duration_ms: float
    created_at: datetime
    processed_at: Optional[datetime] = None
    category_predicted: Optional[str] = None
    category_confidence: Optional[float] = None

    class Config:
        from_attributes = True

class DocumentListParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=100)
    search: Optional[str] = None
    category: Optional[str] = None
    file_type: Optional[str] = None
    status: Optional[str] = None
    sort_by: str = "created_at"
    sort_order: str = "desc"

class DocumentDetailResponse(DocumentResponse):
    extracted_text: Optional[str] = None
    summary_text: Optional[str] = None
    keywords: Optional[List[Dict[str, Any]]] = None
    topics: Optional[List[Dict[str, Any]]] = None
    summary_sentences: Optional[List[Dict[str, Any]]] = None
    key_points: Optional[List[str]] = None
    anomaly_findings: Optional[List[Dict[str, Any]]] = None
    tables: Optional[List[Dict[str, Any]]] = None
    tabular_stats: Optional[Dict[str, Any]] = None
    alternative_categories: Optional[List[Dict[str, Any]]] = None
    similar_documents: Optional[List[Dict[str, Any]]] = None
