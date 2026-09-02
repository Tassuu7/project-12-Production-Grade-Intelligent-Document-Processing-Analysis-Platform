"""Health & Telemetry Endpoints."""
from fastapi import APIRouter, Depends
from app.core.database import check_db_health
from app.services.queue.job_queue import job_queue

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/")
def health_check():
    db_ok = check_db_health()
    return {
        "status": "healthy" if db_ok else "degraded",
        "database": db_ok,
        "queue_size": job_queue.get_queue_size(),
        "running_workers": job_queue.get_running_count()
    }
