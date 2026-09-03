"""Faceted search query and result schemas."""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class SearchQuery(BaseModel):
    q: str = Field(..., min_length=1, max_length=200)
    category: Optional[str] = None
    file_type: Optional[str] = None
    status: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=50)

class SearchResultItem(BaseModel):
    document_id: int
    title: str
    original_filename: str
    file_type: str
    category: str
    confidence: float
    snippet_highlight: str
    match_type: str  # content, keyword, title, topic
    relevance_score: float
    created_at: str
    user_id: Optional[int] = None

class SearchFacet(BaseModel):
    value: str
    count: int

class SearchFacets(BaseModel):
    categories: List[SearchFacet]
    file_types: List[SearchFacet]
    statuses: List[SearchFacet]

class SearchResponse(BaseModel):
    query: str
    total_matches: int
    page: int
    total_pages: int
    results: List[SearchResultItem]
    facets: SearchFacets
