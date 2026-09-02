"""
Processing Job ORM Model for background pipeline lifecycle tracking.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class ProcessingJob(Base, TimestampMixin):
    __tablename__ = "processing_jobs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(50), default="QUEUED", nullable=False, index=True)  # QUEUED, RUNNING, COMPLETED, FAILED, RETRYING, CANCELLED
    priority = Column(Integer, default=0, nullable=False)
    attempts = Column(Integer, default=0, nullable=False)
    max_attempts = Column(Integer, default=3, nullable=False)
    
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration_ms = Column(Float, default=0.0, nullable=False)
    error_message = Column(Text, nullable=True)
    stack_trace = Column(Text, nullable=True)
    worker_id = Column(String(100), nullable=True)

    # Relationships
    document = relationship("Document", back_populates="processing_jobs")
    user = relationship("User", back_populates="processing_jobs")

    def __repr__(self):
        return f"<ProcessingJob id={self.id} doc={self.document_id} status={self.status}>"
