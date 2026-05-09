"""
Budgets feature — API Router
Full CRUD for Budgets and BudgetItems with auth guard.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user_id
from app.features.budgets.models import BudgetPeriod
from app.features.budgets.schemas import (
    BudgetItemCreate,
    BudgetItemResponse,
    BudgetItemUpdate,
    BudgetFilterParams,
    BudgetListResponse,
    BudgetResponse,
    CreateBudgetRequest,
    UpdateBudgetRequest,
)
from app.features.budgets.service import BudgetService

router = APIRouter()


# ── Budgets CRUD ────────────────────────────────────────────────


@router.get("/", response_model=BudgetListResponse)
async def list_budgets(
    year: Optional[int] = Query(default=None),
    month: Optional[int] = Query(default=None),
    period: Optional[BudgetPeriod] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """List budgets dengan filter (year, month, period) dan pagination."""
    filters = BudgetFilterParams(
        year=year, month=month, period=period, page=page, page_size=page_size
    )
    return await BudgetService.list_budgets(db, user_id, filters)


@router.post("/", response_model=BudgetResponse, status_code=201)
async def create_budget(
    payload: CreateBudgetRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Buat budget baru (bisa dengan items sekaligus)."""
    return await BudgetService.create(db, user_id, payload)


@router.get("/{budget_id}", response_model=BudgetResponse)
async def get_budget(
    budget_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Ambil detail budget (termasuk items)."""
    return await BudgetService.get_by_id(db, user_id, budget_id)


@router.patch("/{budget_id}", response_model=BudgetResponse)
async def update_budget(
    budget_id: str,
    payload: UpdateBudgetRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Update detail budget (partial update)."""
    return await BudgetService.update(db, user_id, budget_id, payload)


@router.delete("/{budget_id}", status_code=204)
async def delete_budget(
    budget_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Hapus budget beserta seluruh itemnya (cascade)."""
    await BudgetService.delete(db, user_id, budget_id)


# ── BudgetItem Endpoints ────────────────────────────────────────


@router.post("/{budget_id}/items", response_model=BudgetItemResponse, status_code=201)
async def add_budget_item(
    budget_id: str,
    payload: BudgetItemCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Tambah satu item ke budget yang sudah ada."""
    return await BudgetService.add_item(db, user_id, budget_id, payload)


@router.patch("/items/{item_id}", response_model=BudgetItemResponse)
async def update_budget_item(
    item_id: str,
    payload: BudgetItemUpdate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Update item budget spesifik."""
    return await BudgetService.update_item(db, user_id, item_id, payload)


@router.delete("/items/{item_id}", status_code=204)
async def delete_budget_item(
    item_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Hapus item budget spesifik."""
    await BudgetService.delete_item(db, user_id, item_id)
