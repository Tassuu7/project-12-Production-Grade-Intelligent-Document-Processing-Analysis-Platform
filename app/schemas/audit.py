"""Audit logging schemas."""
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    username: Optional[str] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    severity: str
    details: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True
