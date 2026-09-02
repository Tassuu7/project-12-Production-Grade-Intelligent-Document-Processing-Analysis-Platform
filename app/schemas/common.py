"""Common generic API response schemas."""
from typing import Generic, TypeVar, Optional, Any, List, Dict
from pydantic import BaseModel, Field

DataT = TypeVar("DataT")

class ApiResponse(BaseModel, Generic[DataT]):
    success: bool = Field(True, description="Indicates request success status")
    message: Optional[str] = Field(None, description="Human-readable status or guidance message")
    data: Optional[DataT] = Field(None, description="Response payload")
    error: Optional[str] = Field(None, description="Error explanation if failed")
    status_code: int = Field(200, description="HTTP status code")

class PaginatedMeta(BaseModel):
    total_items: int = Field(..., description="Total items matching filter")
    total_pages: int = Field(..., description="Total pages available")
    current_page: int = Field(..., description="Current 1-indexed page")
    page_size: int = Field(..., description="Items per page")
    has_next: bool = Field(False, description="Whether another page exists")
    has_prev: bool = Field(False, description="Whether previous page exists")

class PaginatedResponse(BaseModel, Generic[DataT]):
    success: bool = True
    items: List[DataT]
    meta: PaginatedMeta
