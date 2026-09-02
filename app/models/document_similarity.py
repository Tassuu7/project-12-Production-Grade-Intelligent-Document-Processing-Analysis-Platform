"""
Document Similarity ORM Model mapping cosine distances between documents.
"""
from sqlalchemy import Column, Integer, ForeignKey, Float, String, Text
from app.core.database import Base
from app.models.base import TimestampMixin

class DocumentSimilarity(Base, TimestampMixin):
    __tablename__ = "document_similarities"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    source_document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    target_document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    similarity_score = Column(Float, nullable=False, index=True)  # 0.0 to 1.0
    shared_terms_json = Column(Text, nullable=True)               # Common overlapping keywords
    calculation_method = Column(String(50), default="TFIDF_COSINE", nullable=False)

    def __repr__(self):
        return f"<DocumentSimilarity {self.source_document_id}->{self.target_document_id}: {self.similarity_score:.2f}>"
