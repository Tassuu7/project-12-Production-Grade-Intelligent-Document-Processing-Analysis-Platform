"""Document Management Business Service."""
import os
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
    def delete_document(db: Session, document_id: int, user_id: int, is_admin: bool = False) -> None:
        doc = DocumentService.get_user_document(db, document_id, user_id, is_admin)
        doc.is_deleted = True
        
        # Decrement user document stats
        user = doc.owner
        if user:
            user.document_count = max(0, user.document_count - 1)
            user.storage_used_bytes = max(0, user.storage_used_bytes - doc.file_size_bytes)
        
        try:
            if doc.file_path and os.path.exists(doc.file_path):
                os.remove(doc.file_path)
        except Exception:
            pass
            
        db.commit()

    @staticmethod
    def update_document(db: Session, document_id: int, title: Optional[str], category: Optional[str], user_id: int, is_admin: bool = False) -> Document:
        doc = DocumentService.get_user_document(db, document_id, user_id, is_admin)
        if title and title.strip():
            doc.title = title.strip()
        if category and category.strip():
            doc.category = category.strip()
            if doc.analysis_result:
                doc.analysis_result.category_predicted = category.strip()
        db.commit()
        db.refresh(doc)
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
