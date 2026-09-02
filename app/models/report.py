"""
Report ORM Model tracking generated PDF, HTML, JSON, and CSV export records.
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class Report(Base, TimestampMixin):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    report_type = Column(String(50), default="document_analysis", nullable=False) # document_analysis, system_summary, audit_export
    format = Column(String(20), default="html", nullable=False)                  # html, pdf, json, csv
    file_path = Column(String(500), nullable=False)
    file_size_bytes = Column(BigInteger, default=0, nullable=False)
    status = Column(String(50), default="COMPLETED", nullable=False)

    # Relationships
    user = relationship("User", back_populates="reports")
    document = relationship("Document", back_populates="reports")

    def __repr__(self):
        return f"<Report id={self.id} title={self.title} format={self.format}>"
