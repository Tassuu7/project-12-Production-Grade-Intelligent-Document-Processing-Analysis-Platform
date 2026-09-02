"""Processing job schemas."""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class JobResponse(BaseModel):
    id: int
    document_id: int
    user_id: int
    status: str
    priority: int
    attempts: int
    max_attempts: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_ms: float
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class JobRetryRequest(BaseModel):
    force: bool = False
