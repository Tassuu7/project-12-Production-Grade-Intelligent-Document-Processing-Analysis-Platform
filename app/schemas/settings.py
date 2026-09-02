"""System settings and health schemas."""
from typing import Optional, Dict, Any
from pydantic import BaseModel

class SystemSettingResponse(BaseModel):
    id: int
    key: str
    value: str
    description: Optional[str] = None
    value_type: str
    is_editable: bool

    class Config:
        from_attributes = True

class SystemSettingUpdate(BaseModel):
    value: str

class SystemHealthResponse(BaseModel):
    status: str
    app_version: str
    uptime_seconds: float
    database_healthy: bool
    worker_pool_active: bool
    queued_jobs_count: int
    running_jobs_count: int
    failed_jobs_count: int
    disk_usage_mb: float
    disk_free_mb: float
    cpu_usage_percent: float
    memory_usage_mb: float
