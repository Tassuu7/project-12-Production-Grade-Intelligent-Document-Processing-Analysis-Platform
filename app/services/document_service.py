"""Document Management Business Service."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.processing_job import ProcessingJob
from app.services.queue.job_queue import job_queue
from app.core.exceptions import DocumentNotFoundException, AuthorizationException

class DocumentService:
    @staticmethod
    def get_user_document(db: Session, document_id: int, user_id: int, is_admin: bool = False) -> Document:
        doc = db.query(Document).filter(Document.id == document_id, Document.is_deleted == False).first()
        if not doc:
            raise DocumentNotFoundException(document_id)
        if not is_admin and doc.user_id != user_id:
            raise AuthorizationException("Access denied to requested document.")
        return doc

    @staticmethod
    def reprocess_document(db: Session, document_id: int, user_id: int, is_admin: bool = False) -> ProcessingJob:
        doc = DocumentService.get_user_document(db, document_id, user_id, is_admin)
        doc.status = "queued"
        
        job = ProcessingJob(
            document_id=doc.id,
            user_id=doc.user_id,
            status="QUEUED",
            priority=1
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        
        job_queue.enqueue(job.id, doc.id, doc.user_id, priority=1)
        return job
