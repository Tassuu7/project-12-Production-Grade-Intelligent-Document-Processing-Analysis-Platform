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
from app.api.dependencies import get_current_user_optional, get_current_admin
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
def index_redirect(request: Request, user: User = Depends(get_current_user_optional)):
    if user:
        if user.role == "admin":
            return RedirectResponse(url="/admin/dashboard")
        return RedirectResponse(url="/dashboard")
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, user: User = Depends(get_current_user_optional)):
    # If explicit switch requested or not logged in, render login page
    if request.query_params.get("switch") or not user:
        return templates.TemplateResponse(request=request, name="login.html", context={})
    # If user already logged in and visiting without switch parameter, direct to respective dashboard
    if user.role == "admin":
        return RedirectResponse(url="/admin/dashboard")
    return RedirectResponse(url="/dashboard")

@app.get("/logout")
def logout_endpoint(request: Request):
    response = RedirectResponse(url="/login?switch=true", status_code=303)
    response.delete_cookie(key="doc_intel_session", path="/")
    response.delete_cookie(key="doc_intel_user_session", path="/")
    response.delete_cookie(key="doc_intel_admin_session", path="/")
    return response

@app.get("/dashboard", response_class=HTMLResponse)
def user_dashboard(request: Request, user: User = Depends(get_current_user_optional), db: Session = Depends(get_db)):
    if not user:
        return RedirectResponse(url="/login?switch=true")
    if user.role == "admin":
        # Check if user session cookie exists for standard user
        user_cookie = request.cookies.get("doc_intel_user_session")
        if not user_cookie:
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
        "stats": stats,
        "recent_docs": docs[:8],
        "category_counts": category_counts,
        "active_page": "dashboard",
        "is_admin": False
    })

@app.get("/upload", response_class=HTMLResponse)
def upload_page(request: Request, user: User = Depends(get_current_user_optional)):
    if not user:
        return RedirectResponse(url="/login?switch=true")
    return templates.TemplateResponse(request=request, name="user/upload.html", context={
        "request": request,
        "user": user,
        "active_page": "upload",
        "is_admin": user.role == "admin"
    })

@app.get("/documents", response_class=HTMLResponse)
def user_documents(request: Request, user: User = Depends(get_current_user_optional), db: Session = Depends(get_db)):
    if not user:
        return RedirectResponse(url="/login?switch=true")
    docs = db.query(Document).filter(Document.user_id == user.id, Document.is_deleted == False).order_by(Document.created_at.desc()).all()
    return templates.TemplateResponse(request=request, name="user/documents.html", context={
        "request": request,
        "user": user,
        "documents": docs,
        "active_page": "documents",
        "is_admin": user.role == "admin"
    })

@app.get("/documents/{document_id}", response_class=HTMLResponse)
def document_detail(document_id: int, request: Request, user: User = Depends(get_current_user_optional), db: Session = Depends(get_db)):
    if not user:
        return RedirectResponse(url="/login?switch=true")
    
    query = db.query(Document).filter(Document.id == document_id, Document.is_deleted == False)
    if user.role != "admin":
        query = query.filter(Document.user_id == user.id)
    doc = query.first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")
        
    analysis = doc.analysis_result
    keywords = []
    topics = []
    anomalies = []
    
    if analysis:
        try:
            if analysis.keywords_json:
                keywords = json.loads(analysis.keywords_json)
        except Exception:
            keywords = []
            
        try:
            if analysis.topics_json:
                topics = json.loads(analysis.topics_json)
        except Exception:
            topics = []
            
        try:
            if analysis.anomaly_findings_json:
                anomalies = json.loads(analysis.anomaly_findings_json)
        except Exception:
            anomalies = []

    # Resume & Candidate Intelligence
    resume_data = None
    category_name = (doc.category or (analysis.category_predicted if analysis else "") or "").lower()
    filename_lower = (doc.original_filename or "").lower()
    
    if "resume" in category_name or "cv" in category_name or "resume" in filename_lower or "cv" in filename_lower:
        try:
            from app.services.nlp.resume_analyzer import ResumeJobAnalyzer
            text_to_analyze = (analysis.extracted_text if analysis and analysis.extracted_text else "") or doc.title
            resume_data = ResumeJobAnalyzer.analyze_candidate_resume(text_to_analyze)
        except Exception as e:
            logger.error(f"Error in resume analyzer: {e}")
            resume_data = None
            
    # Fetch similar documents in user's corpus
    similar_docs = []
    try:
        similarities = db.query(DocumentSimilarity).filter(
            DocumentSimilarity.source_document_id == doc.id
        ).order_by(DocumentSimilarity.similarity_score.desc()).limit(5).all()
        
        for sim in similarities:
            target_doc = db.query(Document).filter(Document.id == sim.target_document_id).first()
            if target_doc:
                shared = json.loads(sim.shared_terms_json) if sim.shared_terms_json else []
                similar_docs.append({
                    "target_id": target_doc.id,
                    "title": target_doc.title,
                    "score": sim.similarity_score,
                    "shared_terms": shared[:4]
                })
    except Exception:
        similar_docs = []
            
    return templates.TemplateResponse(request=request, name="user/document_detail.html", context={
        "request": request,
        "user": user,
        "doc": doc,
        "analysis": analysis,
        "keywords": keywords,
        "topics": topics,
        "anomalies": anomalies,
        "resume_data": resume_data,
        "similar_docs": similar_docs,
        "active_page": "documents",
        "is_admin": user.role == "admin"
    })

@app.get("/search", response_class=HTMLResponse)
def search_page(request: Request, q: str = "", user: User = Depends(get_current_user_optional), db: Session = Depends(get_db)):
    if not user:
        return RedirectResponse(url="/login?switch=true")
    results = []
    if q.strip():
        search_res = SearchService.search(db=db, query=q.strip(), user_id=user.id, is_admin=(user.role == "admin"), limit=30)
        results = search_res.results
    return templates.TemplateResponse(request=request, name="user/search.html", context={
        "request": request,
        "user": user,
        "query": q,
        "results": results,
        "active_page": "search",
        "is_admin": user.role == "admin"
    })

@app.get("/reports", response_class=HTMLResponse)
def reports_page(request: Request, user: User = Depends(get_current_user_optional), db: Session = Depends(get_db)):
    if not user:
        return RedirectResponse(url="/login?switch=true")
    docs = db.query(Document).filter(Document.user_id == user.id, Document.is_deleted == False).order_by(Document.created_at.desc()).all()
    return templates.TemplateResponse(request=request, name="user/reports.html", context={
        "request": request,
        "user": user,
        "documents": docs,
        "active_page": "reports",
        "is_admin": user.role == "admin"
    })

# ==================== ADMIN PORTAL ROUTES ====================

@app.get("/admin/dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request, admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_docs = db.query(Document).filter(Document.is_deleted == False).count()
    total_jobs = db.query(ProcessingJob).count()
    recent_jobs = db.query(ProcessingJob).order_by(ProcessingJob.created_at.desc()).limit(10).all()
    recent_audit = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(10).all()
    
    # Calculate real dynamic category breakdown for admin
    all_docs = db.query(Document).filter(Document.is_deleted == False).all()
    category_counts = {}
    for d in all_docs:
        cat = d.category or (d.analysis_result.category_predicted if d.analysis_result else "General Document")
        category_counts[cat] = category_counts.get(cat, 0) + 1
        
    stats = {
        "total_users": total_users,
        "total_documents": total_docs,
        "total_jobs": total_jobs,
        "completed_jobs": db.query(ProcessingJob).filter(ProcessingJob.status == "completed").count()
    }
    
    return templates.TemplateResponse(request=request, name="admin/dashboard.html", context={
        "request": request,
        "user": admin,
        "stats": stats,
        "admin_stats": stats,
        "category_counts": category_counts,
        "recent_jobs": recent_jobs,
        "recent_audit": recent_audit,
        "active_page": "admin_dash",
        "is_admin": True
    })

@app.get("/admin/users", response_class=HTMLResponse)
def admin_users(request: Request, admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.created_at.desc()).all()
    return templates.TemplateResponse(request=request, name="admin/users.html", context={
        "request": request,
        "user": admin,
        "users": users,
        "active_page": "admin_users",
        "is_admin": True
    })

@app.get("/admin/documents", response_class=HTMLResponse)
def admin_documents(request: Request, admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    docs = db.query(Document).filter(Document.is_deleted == False).order_by(Document.created_at.desc()).all()
    return templates.TemplateResponse(request=request, name="admin/documents.html", context={
        "request": request,
        "user": admin,
        "documents": docs,
        "active_page": "admin_docs",
        "is_admin": True
    })

@app.get("/admin/search", response_class=HTMLResponse)
def admin_search(request: Request, q: str = "", admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    results = []
    if q.strip():
        search_res = SearchService.search(db=db, query=q.strip(), user_id=None, is_admin=True, limit=50)
        results = search_res.results
    return templates.TemplateResponse(request=request, name="admin/search.html", context={
        "request": request,
        "user": admin,
        "query": q,
        "results": results,
        "active_page": "admin_search",
        "is_admin": True
    })

@app.get("/admin/jobs", response_class=HTMLResponse)
def admin_jobs(request: Request, admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    jobs = db.query(ProcessingJob).order_by(ProcessingJob.created_at.desc()).limit(100).all()
    return templates.TemplateResponse(request=request, name="admin/jobs.html", context={
        "request": request,
        "user": admin,
        "jobs": jobs,
        "active_page": "admin_jobs",
        "is_admin": True
    })

@app.get("/admin/audit-logs", response_class=HTMLResponse)
def admin_audit_logs(request: Request, admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(100).all()
    return templates.TemplateResponse(request=request, name="admin/audit_logs.html", context={
        "request": request,
        "user": admin,
        "logs": logs,
        "active_page": "admin_audit",
        "is_admin": True
    })
