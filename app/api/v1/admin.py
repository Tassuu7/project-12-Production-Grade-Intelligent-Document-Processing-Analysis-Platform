"""Admin Command Center Endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.document import Document
from app.models.processing_job import ProcessingJob
from app.models.audit_log import AuditLog
from app.api.dependencies import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/stats")
def get_admin_stats(admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_docs = db.query(Document).count()
    completed_docs = db.query(Document).filter(Document.status == "completed").count()
    failed_docs = db.query(Document).filter(Document.status == "failed").count()
    active_jobs = db.query(ProcessingJob).filter(ProcessingJob.status.in_(["QUEUED", "RUNNING"])).count()
    
    success_rate = round((completed_docs / max(1, completed_docs + failed_docs)) * 100, 1)
    
    return {
        "total_users": total_users,
        "total_documents": total_docs,
        "completed_documents": completed_docs,
        "failed_documents": failed_docs,
        "active_jobs": active_jobs,
        "success_rate": success_rate
    }
