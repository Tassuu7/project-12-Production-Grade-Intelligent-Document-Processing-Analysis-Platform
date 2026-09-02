"""Reports API Endpoints."""
from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response as RawResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.api.dependencies import get_current_user
from app.services.document_service import DocumentService
from app.services.reports.report_generator import ReportGenerator

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/document/{document_id}")
def generate_document_report(
    document_id: int,
    format: str = Query("html", regex="^(html|pdf|json|csv)$"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = DocumentService.get_user_document(db, document_id, user.id, is_admin=(user.role == "admin"))
    fname, content, mime = ReportGenerator.generate_report(doc, format)
    
    disposition = "inline" if format == "html" else f'attachment; filename="{fname}"'
    return RawResponse(content=content, media_type=mime, headers={"Content-Disposition": disposition})
