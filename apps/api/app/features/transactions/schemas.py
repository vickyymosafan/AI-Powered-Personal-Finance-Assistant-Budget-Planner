"""
Transaction feature — Pydantic schemas for request/response validation
"""

from datetime import date as DateType
from typing import Optional

from pydantic import BaseModel, Field

from app.features.transactions.models import TransactionCategory, TransactionType


# ── Request Schemas ──────────────────────────────────────────────


class CreateTransactionRequest(BaseModel):
    type: TransactionType
    category: TransactionCategory
    amount: float = Field(gt=0, description="Harus lebih dari 0")
    description: str | None = Field(default=None, max_length=500)
    date: DateType
    merchant: str | None = Field(default=None, max_length=200)


class UpdateTransactionRequest(BaseModel):
    type: TransactionType | None = None
    category: TransactionCategory | None = None
    amount: float | None = Field(default=None, gt=0)
    description: str | None = Field(default=None, max_length=500)
    date: Optional[DateType] = None
    merchant: str | None = Field(default=None, max_length=200)


class TransactionFilterParams(BaseModel):
    """Query params for filtering transactions."""
    type: TransactionType | None = None
    category: TransactionCategory | None = None
    start_date: Optional[DateType] = None
    end_date: Optional[DateType] = None
    min_amount: float | None = None
    max_amount: float | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


# ── Response Schemas ─────────────────────────────────────────────


class TransactionResponse(BaseModel):
    id: str
    type: str
    category: str
    amount: float
    description: str | None
    date: str
    merchant: str | None
    created_at: str

    model_config = {"from_attributes": True}


class TransactionListResponse(BaseModel):
    items: list[TransactionResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class CategorySummary(BaseModel):
    category: str
    total: float
    count: int
    percentage: float


class TransactionSummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    net_balance: float
    transaction_count: int
    expense_by_category: list[CategorySummary]
    income_by_category: list[CategorySummary]
    period_start: str | None
    period_end: str | None
