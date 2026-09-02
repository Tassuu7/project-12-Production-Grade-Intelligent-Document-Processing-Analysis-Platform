"""
Database Connection, Engine, Sessionmaker, and Schema Management.
"""
import logging
from typing import Generator
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.core.config import settings

logger = logging.getLogger("app.core.database")

connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True
)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if "sqlite" in settings.DATABASE_URL:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
    from app.models.user import User
    from app.models.category import Category
    from app.models.system_setting import SystemSetting
    from app.models.document import Document
    from app.models.processing_job import ProcessingJob
    from app.models.analysis_result import AnalysisResult
    from app.models.document_similarity import DocumentSimilarity
    from app.models.audit_log import AuditLog
    from app.models.report import Report
    from app.core.constants import UserRole, DocumentCategory, CATEGORY_KEYWORDS
    from app.core.security import hash_password
    import json
    
    logger.info("Creating database schema tables...")
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    try:
        admin_email = "admin@test.com"
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        if not existing_admin:
            logger.info("Seeding default Administrator user (admin@test.com)...")
            admin_user = User(
                email=admin_email,
                username="admin",
                full_name="System Administrator",
                hashed_password=hash_password("Admin@12345"),
                role=UserRole.ADMIN.value,
                is_active=True,
                is_verified=True
            )
            db.add(admin_user)
            db.commit()

        user_email = "user@test.com"
        existing_user = db.query(User).filter(User.email == user_email).first()
        if not existing_user:
            logger.info("Seeding default Standard user (user@test.com)...")
            std_user = User(
                email=user_email,
                username="user",
                full_name="Jane Document Analyst",
                hashed_password=hash_password("User@12345"),
                role=UserRole.USER.value,
                is_active=True,
                is_verified=True
            )
            db.add(std_user)
            db.commit()

        for cat in DocumentCategory:
            cat_name = cat.value
            slug = cat_name.lower().replace(" ", "-").replace("/", "-")
            existing_cat = db.query(Category).filter(Category.name == cat_name).first()
            if not existing_cat:
                keywords = CATEGORY_KEYWORDS.get(cat_name, [])
                db.add(Category(
                    name=cat_name,
                    slug=slug,
                    description=f"Standard classification category for {cat_name} documents.",
                    keywords=json.dumps(keywords),
                    is_system=True
                ))
        db.commit()

        defaults = [
            ("max_upload_size_mb", "50", "Maximum document upload size in megabytes", "integer"),
            ("worker_concurrency", "4", "Number of background document processing worker threads", "integer"),
            ("max_retries", "3", "Maximum automatic retry attempts for failed processing jobs", "integer"),
            ("enable_audit_logging", "true", "Enable global security and document activity auditing", "boolean"),
            ("default_summary_length", "4", "Default number of extractive summary sentences", "integer"),
            ("similarity_threshold", "0.15", "Minimum cosine similarity threshold for related documents", "float"),
            ("classification_confidence_min", "0.45", "Confidence threshold below which documents are labeled Other", "float"),
            ("retention_days", "90", "Audit logs and processing history retention in days", "integer"),
        ]
        for k, v, desc, vt in defaults:
            if not db.query(SystemSetting).filter(SystemSetting.key == k).first():
                db.add(SystemSetting(key=k, value=v, description=desc, value_type=vt, is_editable=True))
        db.commit()
        logger.info("Database tables and seed data initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        db.rollback()
        raise e
    finally:
        db.close()

def check_db_health() -> bool:
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return True
    except Exception:
        return False
