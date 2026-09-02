"""
Base ORM mixins and metadata declarations.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, Boolean
from app.core.database import Base

class TimestampMixin:
    """Mixin providing automatic timezone-aware created_at and updated_at timestamps."""
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

class SoftDeleteMixin:
    """Mixin providing soft deletion flag for recoverable records."""
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    deleted_at = Column(DateTime, nullable=True)
