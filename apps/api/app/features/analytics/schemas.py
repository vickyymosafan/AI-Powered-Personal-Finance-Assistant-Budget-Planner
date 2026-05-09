"""
Analytics feature — Pydantic schemas for Savings Goals and Analytics
"""

from datetime import date as DateType
from typing import Optional

from pydantic import BaseModel, Field

from app.features.analytics.models import GoalPriority, GoalStatus


# ── Savings Goal Schemas ─────────────────────────────────────────


class CreateSavingsGoalRequest(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str] = Field(default=None)
    target_amount: float = Field(..., gt=0)
    current_amount: float = Field(default=0.0, ge=0)
    target_date: Optional[DateType] = None
    status: GoalStatus = GoalStatus.ACTIVE
    priority: GoalPriority = GoalPriority.MEDIUM
    ai_plan: Optional[str] = None


class UpdateSavingsGoalRequest(BaseModel):
    name: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None)
    target_amount: Optional[float] = Field(default=None, gt=0)
    current_amount: Optional[float] = Field(default=None, ge=0)
    target_date: Optional[DateType] = None
    status: Optional[GoalStatus] = None
    priority: Optional[GoalPriority] = None
    ai_plan: Optional[str] = None


class SavingsGoalFilterParams(BaseModel):
    status: Optional[GoalStatus] = None
    priority: Optional[GoalPriority] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class SavingsGoalResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    target_amount: float
    current_amount: float
    target_date: Optional[DateType]
    status: str
    priority: str
    ai_plan: Optional[str]
    progress_percentage: float
    remaining_amount: float
    created_at: str

    model_config = {"from_attributes": True}


class SavingsGoalListResponse(BaseModel):
    items: list[SavingsGoalResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# ── Analytics Schemas ────────────────────────────────────────────


class AnalyticsOverviewResponse(BaseModel):
    total_income: float
    total_expense: float
    net_balance: float
    active_goals_count: int
    completed_goals_count: int


class TrendDataPoint(BaseModel):
    period: str  # e.g., '2026-05'
    income: float
    expense: float


class TrendsResponse(BaseModel):
    trends: list[TrendDataPoint]


class CategoryDataPoint(BaseModel):
    category: str
    amount: float
    percentage: float


class CategoriesResponse(BaseModel):
    categories: list[CategoryDataPoint]
