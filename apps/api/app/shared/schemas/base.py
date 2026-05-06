"""
Shared Pydantic schemas for API responses
"""

from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Simple message response"""
    message: str


class PaginationMeta(BaseModel):
    """Pagination metadata"""
    page: int
    per_page: int
    total: int
    total_pages: int


class PaginatedResponse(BaseModel):
    """Base paginated response — extend with specific data type"""
    meta: PaginationMeta


class PaginationParams(BaseModel):
    """Query parameters for pagination"""
    page: int = 1
    per_page: int = 20
    sort_by: str = "created_at"
    sort_order: str = "desc"
