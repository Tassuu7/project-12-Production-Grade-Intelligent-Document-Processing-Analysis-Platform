"""
Document ORM Model storing file metadata, physical location, and processing status.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, ForeignKey, BigInteger, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin, SoftDeleteMixin

class Document(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    category = Column(String(100), default="General Document", nullable=True, index=True)
    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False, unique=True)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(20), nullable=False, index=True)  # pdf, docx, txt, csv, xlsx
    mime_type = Column(String(100), nullable=False)
    file_size_bytes = Column(BigInteger, nullable=False)
    file_hash_sha256 = Column(String(64), nullable=False, index=True)
    
    # Quantitative content metrics
    page_count = Column(Integer, default=1, nullable=False)
    word_count = Column(Integer, default=0, nullable=False)
    character_count = Column(Integer, default=0, nullable=False)
    line_count = Column(Integer, default=0, nullable=False)
    table_count = Column(Integer, default=0, nullable=False)

    # Lifecycle Status
    status = Column(String(50), default="uploaded", nullable=False, index=True) # uploaded, queued, processing, completed, failed, retrying, archived
    error_message = Column(Text, nullable=True)
    processing_duration_ms = Column(Float, default=0.0, nullable=False)
    processed_at = Column(DateTime, nullable=True)

    # Relationships
    owner = relationship("User", back_populates="documents")
    analysis_result = relationship("AnalysisResult", back_populates="document", uselist=False, cascade="all, delete-orphan")
    processing_jobs = relationship("ProcessingJob", back_populates="document", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="document", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Document id={self.id} title={self.title} status={self.status}>"
