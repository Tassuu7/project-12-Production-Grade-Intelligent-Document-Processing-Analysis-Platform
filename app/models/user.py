"""
User ORM Model for User and Admin accounts.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="user", nullable=False, index=True) # "user" or "admin"
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    is_verified = Column(Boolean, default=True, nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    storage_used_bytes = Column(BigInteger, default=0, nullable=False)
    document_count = Column(Integer, default=0, nullable=False)

    # Relationships
    documents = relationship("Document", back_populates="owner", cascade="all, delete-orphan")
    processing_jobs = relationship("ProcessingJob", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user")
    reports = relationship("Report", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User id={self.id} email={self.email} role={self.role}>"
