"""Document Upload, Details, Download, Reprocess, and Delete Endpoints."""
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, Response, Query
from fastapi.responses import Response as RawResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.document import Document
from app.models.processing_job import ProcessingJob
from app.schemas.document import DocumentResponse
from app.api.dependencies import get_current_user
from app.services.storage.validator import DocumentValidator
from app.services.storage.file_storage import FileStorageManager
from app.services.document_service import DocumentService
from app.services.audit_service import AuditService
from app.services.queue.job_queue import job_queue

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=List[DocumentResponse])
async def upload_documents(
    files: List[UploadFile] = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    storage = FileStorageManager()
    created_docs = []
    
    for upload in files:
        ext = DocumentValidator.validate_file_extension(upload.filename)
        save_info = storage.save_upload(upload.file, upload.filename, user.id)
        
        # Check duplicate SHA-256 for this user
        existing = db.query(Document).filter(
            Document.user_id == user.id,
            Document.file_hash_sha256 == save_info["file_hash_sha256"],
            Document.is_deleted == False
        ).first()
        
        if existing:
            created_docs.append(existing)
            continue
            
        doc = Document(
            user_id=user.id,
            title=upload.filename.rsplit(".", 1)[0].replace("_", " ").title(),
            original_filename=upload.filename,
            stored_filename=save_info["stored_filename"],
            file_path=save_info["file_path"],
            file_type=ext,
            mime_type=upload.content_type or "application/octet-stream",
            file_size_bytes=save_info["file_size_bytes"],
            file_hash_sha256=save_info["file_hash_sha256"],
            status="queued"
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        
        # Create processing job
        job = ProcessingJob(
            document_id=doc.id,
            user_id=user.id,
            status="QUEUED"
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        
        # Update user storage stats
        user.document_count += 1
        user.storage_used_bytes += doc.file_size_bytes
        db.commit()
        
        job_queue.enqueue(job.id, doc.id, user.id)
        AuditService.log_event(db, "DOCUMENT_UPLOAD", "DOCUMENT", user_id=user.id, resource_id=str(doc.id))
        created_docs.append(doc)
        
    return created_docs

@router.get("/", response_model=List[DocumentResponse])
def list_documents(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Document).filter(Document.user_id == user.id, Document.is_deleted == False).all()

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return DocumentService.get_user_document(db, document_id, user.id, is_admin=(user.role == "admin"))

@router.get("/{document_id}/download")
def download_document(document_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    doc = DocumentService.get_user_document(db, document_id, user.id, is_admin=(user.role == "admin"))
    storage = FileStorageManager()
    content = storage.get_file_bytes(doc.file_path)
    AuditService.log_event(db, "DOCUMENT_DOWNLOAD", "DOCUMENT", user_id=user.id, resource_id=str(doc.id))
    return RawResponse(
        content=content,
        media_type=doc.mime_type,
        headers={"Content-Disposition": f'attachment; filename="{doc.original_filename}"'}
    )

@router.post("/{document_id}/reprocess")
def reprocess_document(document_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    job = DocumentService.reprocess_document(db, document_id, user.id, is_admin=(user.role == "admin"))
    AuditService.log_event(db, "DOCUMENT_REPROCESS", "DOCUMENT", user_id=user.id, resource_id=str(document_id))
    return {"message": "Document re-enqueued for analysis.", "job_id": job.id}
