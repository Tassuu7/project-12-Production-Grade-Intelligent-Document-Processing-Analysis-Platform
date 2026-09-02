"""
Audit Log ORM Model recording all authenticated user and administrator operations.
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(String(100), nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
    severity = Column(String(20), default="INFO", nullable=False, index=True) # INFO, WARNING, ERROR, CRITICAL
    details_json = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog id={self.id} action={self.action} user={self.user_id}>"
