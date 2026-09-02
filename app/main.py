"""
FastAPI Application Entrypoint, Route Registrations, Middleware Mounting, and Startup Lifecycle.
"""
import json
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.config import settings, BASE_DIR
from app.core.database import get_db, init_db
from app.core.logging_config import setup_logging
from app.core.middleware import ProcessTimerAndSecurityMiddleware
from app.api.v1 import api_v1_router
from app.api.dependencies import get_current_user_optional
from app.services.queue.worker import worker_pool
from app.models.user import User
from app.models.document import Document
from app.models.processing_job import ProcessingJob
from app.models.audit_log import AuditLog
from app.models.document_similarity import DocumentSimilarity
from app.services.search.search_service import SearchService

setup_logging()
logger = logging.getLogger("app.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Intelligent Document Processing Platform...")
    init_db()
    worker_pool.start()
    yield
    logger.info("Shutting down background workers...")
    worker_pool.stop()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan
)

# Mount Middlewares
app.add_middleware(ProcessTimerAndSecurityMiddleware)

# Mount Static Files & Templates
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "app" / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

# Mount API Routers
app.include_router(api_v1_router)

# ==================== HTML FRONTEND ROUTES ====================

@app.get("/", response_class=HTMLResponse)
def index_redirect(user: User = Depends(get_current_user_optional)):
    if user:
        if user.role == "admin":
            return RedirectResponse(url="/admin/dashboard")
        return RedirectResponse(url="/dashboard")
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, user: User = Depends(get_current_user_optional)):
    if user:
        return RedirectResponse(url="/admin/dashboard" if user.role == "admin" else "/dashboard")
    return templates.TemplateResponse(request=request, name="login.html", context={})

@app.get("/logout")
def logout_endpoint():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="doc_intel_session", path="/")
    return response

@app.get("/dashboard", response_class=HTMLResponse)
def user_dashboard(request: Request, user: User = Depends(get_current_user_optional), db: Session = Depends(get_db)):
    if not user:
        return RedirectResponse(url="/login")
    if user.role == "admin":
        return RedirectResponse(url="/admin/dashboard")
        
    docs = db.query(Document).filter(Document.user_id == user.id, Document.is_deleted == False).order_by(Document.created_at.desc()).all()
    stats = {
        "total_documents": len(docs),
        "completed_documents": len([d for d in docs if d.status == "completed"]),
        "processing_documents": len([d for d in docs if d.status in ["queued", "processing"]])
    }
    
    # Calculate real dynamic category distribution
    category_counts = {}
    for d in docs:
        cat = d.category or (d.analysis_result.category_predicted if d.analysis_result else "General Document")
        category_counts[cat] = category_counts.get(cat, 0) + 1
        
    return templates.TemplateResponse(request=request, name="user/dashboard.html", context={
        "request": request,
        "user": user,
        "is_admin": False,
        "active_page": "dashboard",
        "stats": stats,
        "category_counts": category_counts,
        "recent_docs": docs[:8]
    })

@app.get("/upload", response_class=HTMLResponse)
def upload_page(request: Request, user: User = Depends(get_current_user_optional)):
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse(request=request, name="user/upload.html", context={
        "request": request,
        "user": user,
        "is_admin": (user.role == "admin"),
        "active_page": "upload"
    })

@app.get("/documents", response_class=HTMLResponse)
def user_documents(request: Request, user: User = Depends(get_current_user_optional), db: Session = Depends(get_db)):
    if not user:
        return RedirectResponse(url="/login")
    docs = db.query(Document).filter(Document.user_id == user.id, Document.is_deleted == False).order_by(Document.created_at.desc()).all()
    return templates.TemplateResponse(request=request, name="user/documents.html", context={
        "request": request,
        "user": user,
        "is_admin": (user.role == "admin"),
        "active_page": "documents",
        "documents": docs
    })

@app.get("/documents/{document_id}", response_class=HTMLResponse)
def document_detail_view(document_id: int, request: Request, user: User = Depends(get_current_user_optional), db: Session = Depends(get_db)):
    if not user:
        return RedirectResponse(url="/login")
    doc = db.query(Document).filter(Document.id == document_id, Document.is_deleted == False).first()
    if not doc or (user.role != "admin" and doc.user_id != user.id):
        raise HTTPException(status_code=404, detail="Document not found.")
        
    if doc.status in ["queued", "processing"] or not doc.analysis_result:
        from app.services.queue.task_runner import execute_processing_job
        job = db.query(ProcessingJob).filter(ProcessingJob.document_id == doc.id).order_by(ProcessingJob.id.desc()).first()
        if job:
            execute_processing_job(job.id, doc.id, doc.user_id)
            db.refresh(doc)

    res = doc.analysis_result
    keywords = json.loads(res.keywords_json) if res and res.keywords_json else []
    topics = json.loads(res.topics_json) if res and res.topics_json else []
    tables = json.loads(res.tables_data_json) if res and res.tables_data_json else []
    anomalies = json.loads(res.anomaly_findings_json) if res and res.anomaly_findings_json else []
    resume_data = json.loads(res.readability_scores_json) if res and res.readability_scores_json else None
    
    sim_records = db.query(DocumentSimilarity).filter(DocumentSimilarity.source_document_id == doc.id).all()
    similar_docs = []
    for s in sim_records:
        t_doc = db.query(Document).filter(Document.id == s.target_document_id).first()
        if t_doc:
            similar_docs.append({
                "target_id": t_doc.id,
                "title": t_doc.title,
                "score": s.similarity_score,
                "shared_terms": json.loads(s.shared_terms_json) if s.shared_terms_json else []
            })
            
    return templates.TemplateResponse(request=request, name="user/document_detail.html", context={
        "request": request,
        "user": user,
        "is_admin": (user.role == "admin"),
        "active_page": "documents",
        "doc": doc,
        "keywords": keywords,
        "topics": topics,
        "tables": tables,
        "anomalies": anomalies,
        "similar_docs": similar_docs,
        "resume_data": resume_data
    })

@app.get("/search", response_class=HTMLResponse)
def search_view(request: Request, q: str = "", user: User = Depends(get_current_user_optional), db: Session = Depends(get_db)):
    if not user:
        return RedirectResponse(url="/login")
    results = []
    if q.strip():
        svc = SearchService()
        search_res = svc.search(db, q.strip(), user_id=user.id, is_admin=(user.role == "admin"))
        results = search_res.results
    return templates.TemplateResponse(request=request, name="user/search.html", context={
        "request": request,
        "user": user,
        "is_admin": (user.role == "admin"),
        "active_page": "search",
        "query": q,
        "results": results
    })

@app.get("/reports", response_class=HTMLResponse)
def reports_view(request: Request, user: User = Depends(get_current_user_optional), db: Session = Depends(get_db)):
    if not user:
        return RedirectResponse(url="/login")
    docs = db.query(Document).filter(Document.user_id == user.id, Document.is_deleted == False).all()
    return templates.TemplateResponse(request=request, name="user/reports.html", context={
        "request": request,
        "user": user,
        "is_admin": (user.role == "admin"),
        "active_page": "reports",
        "documents": docs
    })

# ==================== ADMIN HTML ROUTES ====================

@app.get("/admin/dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request, user: User = Depends(get_current_user_optional), db: Session = Depends(get_db)):
    if not user or user.role != "admin":
        return RedirectResponse(url="/login")
        
    total_users = db.query(User).count()
    total_docs = db.query(Document).filter(Document.is_deleted == False).count()
    comp_docs = db.query(Document).filter(Document.status == "completed", Document.is_deleted == False).count()
    fail_docs = db.query(Document).filter(Document.status == "failed", Document.is_deleted == False).count()
    act_jobs = db.query(ProcessingJob).filter(ProcessingJob.status.in_(["QUEUED", "RUNNING"])).count()
    
    stats = {
        "total_users": total_users,
        "total_documents": total_docs,
        "active_jobs": act_jobs,
        "success_rate": round((comp_docs / max(1, comp_docs + fail_docs)) * 100, 1)
    }
    recent_logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(15).all()
    
    return templates.TemplateResponse(request=request, name="admin/dashboard.html", context={
        "request": request,
        "user": user,
        "is_admin": True,
        "active_page": "admin_dash",
        "admin_stats": stats,
        "recent_logs": recent_logs
    })

@app.get("/admin/users", response_class=HTMLResponse)
def admin_users(request: Request, user: User = Depends(get_current_user_optional), db: Session = Depends(get_db)):
    if not user or user.role != "admin":
        return RedirectResponse(url="/login")
    users = db.query(User).all()
    return templates.TemplateResponse(request=request, name="admin/users.html", context={
        "request": request,
        "user": user,
        "is_admin": True,
        "active_page": "admin_users",
        "users": users
    })

@app.get("/admin/documents", response_class=HTMLResponse)
def admin_documents(request: Request, user: User = Depends(get_current_user_optional), db: Session = Depends(get_db)):
    if not user or user.role != "admin":
        return RedirectResponse(url="/login")
    docs = db.query(Document).filter(Document.is_deleted == False).order_by(Document.created_at.desc()).all()
    return templates.TemplateResponse(request=request, name="admin/documents.html", context={
        "request": request,
        "user": user,
        "is_admin": True,
        "active_page": "admin_docs",
        "documents": docs
    })

@app.get("/admin/search", response_class=HTMLResponse)
def admin_search_view(request: Request, q: str = "", user: User = Depends(get_current_user_optional), db: Session = Depends(get_db)):
    if not user or user.role != "admin":
        return RedirectResponse(url="/login")
    results = []
    if q.strip():
        svc = SearchService()
        search_res = svc.search(db, q.strip(), user_id=None, is_admin=True)
        results = search_res.results
    return templates.TemplateResponse(request=request, name="admin/search.html", context={
        "request": request,
        "user": user,
        "is_admin": True,
        "active_page": "admin_search",
        "query": q,
        "results": results
    })

@app.get("/admin/jobs", response_class=HTMLResponse)
def admin_jobs(request: Request, user: User = Depends(get_current_user_optional), db: Session = Depends(get_db)):
    if not user or user.role != "admin":
        return RedirectResponse(url="/login")
    jobs = db.query(ProcessingJob).order_by(ProcessingJob.created_at.desc()).limit(50).all()
    return templates.TemplateResponse(request=request, name="admin/jobs.html", context={
        "request": request,
        "user": user,
        "is_admin": True,
        "active_page": "admin_jobs",
        "jobs": jobs
    })

@app.get("/admin/audit-logs", response_class=HTMLResponse)
def admin_audit_logs(request: Request, user: User = Depends(get_current_user_optional), db: Session = Depends(get_db)):
    if not user or user.role != "admin":
        return RedirectResponse(url="/login")
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(100).all()
    return templates.TemplateResponse(request=request, name="admin/audit_logs.html", context={
        "request": request,
        "user": user,
        "is_admin": True,
        "active_page": "admin_audit",
        "logs": logs
    })
