"""Search API Endpoints."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.search import SearchResponse
from app.api.dependencies import get_current_user
from app.services.search.search_service import SearchService

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/", response_model=SearchResponse)
def execute_search(
    q: str = Query(..., min_length=1),
    category: Optional[str] = None,
    file_type: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    search_svc = SearchService()
    return search_svc.search(
        db=db,
        query=q,
        user_id=user.id,
        is_admin=(user.role == "admin"),
        category=category,
        file_type=file_type,
        page=page,
        limit=limit
    )
