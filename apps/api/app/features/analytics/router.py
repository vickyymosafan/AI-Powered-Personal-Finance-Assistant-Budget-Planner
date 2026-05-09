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
    CreateSavingsGoalRequest,
    SavingsGoalFilterParams,
    SavingsGoalListResponse,
    SavingsGoalResponse,
    UpdateSavingsGoalRequest,
)
from app.features.analytics.service import SavingsGoalService

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


# ── Analytics Stubs ─────────────────────────────────────────────


@router.get("/overview")
async def get_overview():
    """Get analytics overview — to be implemented"""
    return {"message": "Analytics overview"}


@router.get("/spending")
async def get_spending():
    """Get spending analytics — to be implemented"""
    return {"message": "Spending analytics"}


@router.get("/trends")
async def get_trends():
    """Get trend analytics — to be implemented"""
    return {"message": "Trend analytics"}


@router.get("/categories")
async def get_categories():
    """Get category analytics — to be implemented"""
    return {"message": "Category analytics"}
