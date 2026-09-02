"""Analysis results schemas for ML, NLP, and anomalies."""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class KeywordItem(BaseModel):
    term: str
    score: float
    frequency: int

class TopicItem(BaseModel):
    name: str
    score: float
    top_terms: List[str]

class AnomalyItem(BaseModel):
    type: str
    description: str
    severity: str  # LOW, MEDIUM, HIGH
    location: Optional[str] = None

class SimilarityItem(BaseModel):
    target_document_id: int
    target_title: str
    target_category: str
    similarity_score: float
    shared_terms: List[str]

class AnalysisResponse(BaseModel):
    document_id: int
    category: str
    confidence: float
    alternative_categories: List[Dict[str, float]]
    keywords: List[KeywordItem]
    topics: List[TopicItem]
    summary: str
    key_points: List[str]
    anomalies: List[AnomalyItem]
    word_count: int
    page_count: int
    table_count: int
