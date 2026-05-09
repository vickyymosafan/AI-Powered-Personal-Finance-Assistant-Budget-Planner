"""
Budget feature — Pydantic schemas for request/response validation
"""

from typing import Optional

from pydantic import BaseModel, Field, conint

from app.features.budgets.models import BudgetPeriod


# ── BudgetItem Schemas ───────────────────────────────────────────


class BudgetItemCreate(BaseModel):
    category: str = Field(..., max_length=50)
    allocated_amount: float = Field(default=0.0, ge=0)
    spent_amount: float = Field(default=0.0, ge=0)
    ai_recommendation: Optional[str] = None


class BudgetItemUpdate(BaseModel):
    category: Optional[str] = Field(default=None, max_length=50)
    allocated_amount: Optional[float] = Field(default=None, ge=0)
    spent_amount: Optional[float] = Field(default=None, ge=0)
    ai_recommendation: Optional[str] = None


class BudgetItemResponse(BaseModel):
    id: str
    budget_id: str
    category: str
    allocated_amount: float
    spent_amount: float
    ai_recommendation: Optional[str]
    remaining: float
    usage_percentage: float
    created_at: str

    model_config = {"from_attributes": True}


# ── Budget Schemas ───────────────────────────────────────────────


class CreateBudgetRequest(BaseModel):
    name: str = Field(..., max_length=100)
    period: BudgetPeriod = BudgetPeriod.MONTHLY
    year: int = Field(..., ge=2000, le=2100)
    month: int = Field(..., ge=1, le=12)
    total_income: float = Field(default=0.0, ge=0)
    total_budget: float = Field(default=0.0, ge=0)
    ai_notes: Optional[str] = None
    items: list[BudgetItemCreate] = Field(default_factory=list)


class UpdateBudgetRequest(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    period: Optional[BudgetPeriod] = None
    year: Optional[int] = Field(default=None, ge=2000, le=2100)
    month: Optional[int] = Field(default=None, ge=1, le=12)
    total_income: Optional[float] = Field(default=None, ge=0)
    total_budget: Optional[float] = Field(default=None, ge=0)
    ai_notes: Optional[str] = None


class BudgetFilterParams(BaseModel):
    """Query params for filtering budgets."""
    year: Optional[int] = None
    month: Optional[int] = None
    period: Optional[BudgetPeriod] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class BudgetResponse(BaseModel):
    id: str
    name: str
    period: str
    year: int
    month: int
    total_income: float
    total_budget: float
    ai_notes: Optional[str]
    items: list[BudgetItemResponse] = []
    created_at: str

    model_config = {"from_attributes": True}


class BudgetListResponse(BaseModel):
    items: list[BudgetResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
