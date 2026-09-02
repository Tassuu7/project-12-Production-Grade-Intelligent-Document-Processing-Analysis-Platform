"""Category request and response schemas."""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    keywords: Optional[List[str]] = []
    color_code: str = "#2563eb"

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[List[str]] = None
    color_code: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    slug: str
    is_system: bool
    created_at: datetime

    class Config:
        from_attributes = True
