"""
Analysis Result ORM Model storing extracted text, ML classifications,
keywords, topics, extractive summaries, tables, and anomaly indicators.
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class AnalysisResult(Base, TimestampMixin):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    
    # Extracted Plaintext and Structure
    extracted_text = Column(Text, nullable=False)
    extracted_structure_json = Column(Text, nullable=True)  # Headings, paragraphs, sections
    tables_data_json = Column(Text, nullable=True)           # Extracted tabular matrices
    
    # Classification & ML
    category_predicted = Column(String(100), default="General Document", nullable=False, index=True)
    category_confidence = Column(Float, default=0.0, nullable=False)
    alternative_categories_json = Column(Text, nullable=True)  # JSON array of {category, confidence}
    classifier_version = Column(String(50), default="1.0.0", nullable=False)
    
    # NLP Insights
    keywords_json = Column(Text, nullable=True)         # JSON array of {term, score, frequency}
    topics_json = Column(Text, nullable=True)           # JSON array of {topic_name, score, terms}
    summary_text = Column(Text, nullable=True)          # Extractive summary paragraph
    summary_sentences_json = Column(Text, nullable=True)# JSON array of top ranked sentences
    key_points_json = Column(Text, nullable=True)       # JSON array of extracted key takeaways
    
    # Quality & Anomaly Indicators
    anomaly_findings_json = Column(Text, nullable=True) # JSON array of {anomaly_type, description, severity, location}
    tabular_stats_json = Column(Text, nullable=True)    # For CSV/XLSX: column stats, missing count, distributions
    readability_scores_json = Column(Text, nullable=True)# Flesch-Kincaid, ARI, word length distributions
    
    # Document relationships
    document = relationship("Document", back_populates="analysis_result")

    def __repr__(self):
        return f"<AnalysisResult id={self.id} doc={self.document_id} category={self.category_predicted}>"
