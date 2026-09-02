"""Report generation schemas."""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class ReportGenerateRequest(BaseModel):
    document_id: Optional[int] = None
    report_type: str = Field("document_analysis", description="document_analysis, system_summary, audit_export")
    format: str = Field("html", description="html, pdf, json, csv")
    title: Optional[str] = None

class ReportResponse(BaseModel):
    id: int
    user_id: int
    document_id: Optional[int] = None
    title: str
    report_type: str
    format: str
    file_size_bytes: int
    download_url: str
    created_at: datetime

    class Config:
        from_attributes = True
