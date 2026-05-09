"""
Analytics feature — API Router
Includes Savings Goals CRUD and Analytics endpoints.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user_id
from app.features.analytics.models import GoalPriority, GoalStatus
from app.features.analytics.schemas import (
    AnalyticsOverviewResponse,
    CategoriesResponse,
    CreateSavingsGoalRequest,
    SavingsGoalFilterParams,
    SavingsGoalListResponse,
    SavingsGoalResponse,
    TrendsResponse,
    UpdateSavingsGoalRequest,
)
from app.features.analytics.service import AnalyticsService, SavingsGoalService

router = APIRouter()


# ── Savings Goals CRUD ──────────────────────────────────────────


@router.get("/goals", response_model=SavingsGoalListResponse)
async def list_savings_goals(
    status: Optional[GoalStatus] = Query(default=None),
    priority: Optional[GoalPriority] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """List savings goals dengan filter dan pagination."""
    filters = SavingsGoalFilterParams(
        status=status, priority=priority, page=page, page_size=page_size
    )
    return await SavingsGoalService.list_goals(db, user_id, filters)


@router.post("/goals", response_model=SavingsGoalResponse, status_code=201)
async def create_savings_goal(
    payload: CreateSavingsGoalRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Buat target tabungan baru."""
    return await SavingsGoalService.create(db, user_id, payload)


@router.get("/goals/{goal_id}", response_model=SavingsGoalResponse)
async def get_savings_goal(
    goal_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Ambil detail target tabungan."""
    return await SavingsGoalService.get_by_id(db, user_id, goal_id)


@router.patch("/goals/{goal_id}", response_model=SavingsGoalResponse)
async def update_savings_goal(
    goal_id: str,
    payload: UpdateSavingsGoalRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Update detail target tabungan (partial update)."""
    return await SavingsGoalService.update(db, user_id, goal_id, payload)


@router.delete("/goals/{goal_id}", status_code=204)
async def delete_savings_goal(
    goal_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Hapus target tabungan."""
    await SavingsGoalService.delete(db, user_id, goal_id)


# ── Analytics Endpoints ─────────────────────────────────────────


@router.get("/overview", response_model=AnalyticsOverviewResponse)
async def get_overview(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get analytics overview: total income, total expense, active/completed goals count."""
    return await AnalyticsService.get_overview(db, user_id)


@router.get("/trends", response_model=TrendsResponse)
async def get_trends(
    year: int = Query(..., description="Tahun untuk melihat tren"),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get trend bulanan untuk income dan expense pada tahun tertentu."""
    return await AnalyticsService.get_trends(db, user_id, year)


@router.get("/categories", response_model=CategoriesResponse)
async def get_categories(
    year: int = Query(..., description="Tahun"),
    month: int = Query(..., description="Bulan (1-12)", ge=1, le=12),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get proporsi pengeluaran berdasarkan kategori untuk bulan tertentu."""
    return await AnalyticsService.get_spending_categories(db, user_id, year, month)
