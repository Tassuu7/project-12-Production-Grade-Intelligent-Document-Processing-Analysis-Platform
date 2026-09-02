"""Pydantic Schemas package index."""
from app.schemas.common import ApiResponse, PaginatedResponse, PaginatedMeta
from app.schemas.user import UserRegister, UserLogin, UserResponse, UserProfileUpdate, PasswordChangeRequest, UserAdminCreate, UserAdminUpdate, TokenResponse
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.schemas.document import DocumentResponse, DocumentListParams, DocumentDetailResponse
from app.schemas.job import JobResponse, JobRetryRequest
from app.schemas.analysis import AnalysisResponse, KeywordItem, TopicItem, AnomalyItem, SimilarityItem
from app.schemas.search import SearchQuery, SearchResultItem, SearchResponse, SearchFacets, SearchFacet
from app.schemas.audit import AuditLogResponse
from app.schemas.settings import SystemSettingResponse, SystemSettingUpdate, SystemHealthResponse
from app.schemas.report import ReportGenerateRequest, ReportResponse

__all__ = [
    "ApiResponse",
    "PaginatedResponse",
    "PaginatedMeta",
    "UserRegister",
    "UserLogin",
    "UserResponse",
    "UserProfileUpdate",
    "PasswordChangeRequest",
    "UserAdminCreate",
    "UserAdminUpdate",
    "TokenResponse",
    "CategoryCreate",
    "CategoryUpdate",
    "CategoryResponse",
    "DocumentResponse",
    "DocumentListParams",
    "DocumentDetailResponse",
    "JobResponse",
    "JobRetryRequest",
    "AnalysisResponse",
    "KeywordItem",
    "TopicItem",
    "AnomalyItem",
    "SimilarityItem",
    "SearchQuery",
    "SearchResultItem",
    "SearchResponse",
    "SearchFacets",
    "SearchFacet",
    "AuditLogResponse",
    "SystemSettingResponse",
    "SystemSettingUpdate",
    "SystemHealthResponse",
    "ReportGenerateRequest",
    "ReportResponse",
]
