"""
Strongly typed Application Settings and runtime configurations.
"""
import os
from pathlib import Path
from typing import List, Set
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    APP_NAME: str = "Intelligent Document Processing & Analysis Platform"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Enterprise-grade local document intelligence, classification, and analysis platform."
    APP_ENV: str = "development"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    SECRET_KEY: str = "production-secure-random-secret-key-replace-in-production-use-256bit-min-length-key-32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SESSION_COOKIE_NAME: str = "doc_intel_session"
    SESSION_COOKIE_SECURE: bool = False
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "lax"

    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/data/database/doc_intel.db"
    DATABASE_ECHO: bool = False
    DATABASE_CONNECT_TIMEOUT: int = 30

    DATA_DIR: Path = BASE_DIR / "data"
    UPLOAD_DIR: Path = BASE_DIR / "data" / "uploads"
    PROCESSED_DIR: Path = BASE_DIR / "data" / "processed"
    REPORTS_DIR: Path = BASE_DIR / "data" / "reports"
    DATABASE_DIR: Path = BASE_DIR / "data" / "database"
    LOGS_DIR: Path = BASE_DIR / "logs"
    SAMPLE_DOCS_DIR: Path = BASE_DIR / "sample_documents"

    MAX_UPLOAD_SIZE_BYTES: int = 50 * 1024 * 1024
    ALLOWED_EXTENSIONS: Set[str] = {"pdf", "docx", "txt", "csv", "xlsx"}
    MAX_SIMULTANEOUS_UPLOADS: int = 10

    WORKER_CONCURRENCY: int = 4
    MAX_JOB_RETRIES: int = 3
    JOB_TIMEOUT_SECONDS: int = 300
    JOB_POLL_INTERVAL_SECONDS: float = 0.5

    CLASSIFICATION_CONFIDENCE_THRESHOLD: float = 0.45
    DEFAULT_SUMMARY_SENTENCES_COUNT: int = 4
    MAX_KEYWORDS_EXTRACT: int = 15
    MAX_TOPICS_EXTRACT: int = 5
    SIMILARITY_MIN_THRESHOLD: float = 0.15
    REPETITION_ANOMALY_THRESHOLD: float = 0.40
    SHORT_DOCUMENT_CHAR_THRESHOLD: int = 50

    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: Path = BASE_DIR / "logs" / "app.log"
    ENABLE_AUDIT_LOGGING: bool = True
    AUDIT_RETENTION_DAYS: int = 90
    RATE_LIMIT_PER_MINUTE: int = 120

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()

settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
settings.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
settings.DATABASE_DIR.mkdir(parents=True, exist_ok=True)
settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)
settings.SAMPLE_DOCS_DIR.mkdir(parents=True, exist_ok=True)
