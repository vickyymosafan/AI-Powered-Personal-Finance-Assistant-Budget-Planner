"""
Analytics feature — Business logic service
Handles CRUD operations for Savings Goals and analytics logic.
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenError, NotFoundError
from app.features.analytics.models import SavingsGoal
from app.features.analytics.schemas import (
    CreateSavingsGoalRequest,
    SavingsGoalFilterParams,
    SavingsGoalListResponse,
    SavingsGoalResponse,
    UpdateSavingsGoalRequest,
)


def _goal_to_response(goal: SavingsGoal) -> SavingsGoalResponse:
    return SavingsGoalResponse(
        id=goal.id,
        name=goal.name,
        description=goal.description,
        target_amount=goal.target_amount,
        current_amount=goal.current_amount,
        target_date=goal.target_date,
        status=goal.status.value,
        priority=goal.priority.value,
        ai_plan=goal.ai_plan,
        progress_percentage=goal.progress_percentage,
        remaining_amount=goal.remaining_amount,
        created_at=goal.created_at.isoformat(),
    )


class SavingsGoalService:
    """Stateless service for Savings Goals."""

    @staticmethod
    async def create(
        db: AsyncSession, user_id: str, payload: CreateSavingsGoalRequest
    ) -> SavingsGoalResponse:
        """Create a new savings goal."""
        goal = SavingsGoal(
            user_id=user_id,
            name=payload.name,
            description=payload.description,
            target_amount=payload.target_amount,
            current_amount=payload.current_amount,
            target_date=payload.target_date,
            status=payload.status,
            priority=payload.priority,
            ai_plan=payload.ai_plan,
        )
        db.add(goal)
        await db.flush()
        await db.refresh(goal)
        return _goal_to_response(goal)

    @staticmethod
    async def get_by_id(
        db: AsyncSession, user_id: str, goal_id: str
    ) -> SavingsGoalResponse:
        """Get a single savings goal by ID."""
        goal = await db.get(SavingsGoal, goal_id)
        if goal is None:
            raise NotFoundError(detail="Savings goal tidak ditemukan")
        if goal.user_id != user_id:
            raise ForbiddenError(detail="Akses ditolak")
        return _goal_to_response(goal)

    @staticmethod
    async def update(
        db: AsyncSession, user_id: str, goal_id: str, payload: UpdateSavingsGoalRequest
    ) -> SavingsGoalResponse:
        """Update a savings goal (partial update)."""
        goal = await db.get(SavingsGoal, goal_id)
        if goal is None:
            raise NotFoundError(detail="Savings goal tidak ditemukan")
        if goal.user_id != user_id:
            raise ForbiddenError(detail="Akses ditolak")

        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(goal, field, value)

        await db.flush()
        await db.refresh(goal)
        return _goal_to_response(goal)

    @staticmethod
    async def delete(db: AsyncSession, user_id: str, goal_id: str) -> None:
        """Delete a savings goal."""
        goal = await db.get(SavingsGoal, goal_id)
        if goal is None:
            raise NotFoundError(detail="Savings goal tidak ditemukan")
        if goal.user_id != user_id:
            raise ForbiddenError(detail="Akses ditolak")
        
        await db.delete(goal)
        await db.flush()

    @staticmethod
    async def list_goals(
        db: AsyncSession, user_id: str, filters: SavingsGoalFilterParams
    ) -> SavingsGoalListResponse:
        """List savings goals with filtering and pagination."""
        base = select(SavingsGoal).where(SavingsGoal.user_id == user_id)

        if filters.status is not None:
            base = base.where(SavingsGoal.status == filters.status)
        if filters.priority is not None:
            base = base.where(SavingsGoal.priority == filters.priority)

        # Count
        count_stmt = select(func.count()).select_from(base.subquery())
        total = (await db.execute(count_stmt)).scalar() or 0

        # Pagination
        offset = (filters.page - 1) * filters.page_size
        items_stmt = (
            base.order_by(SavingsGoal.created_at.desc())
            .offset(offset)
            .limit(filters.page_size)
        )
        result = await db.execute(items_stmt)
        items = [_goal_to_response(g) for g in result.scalars().all()]

        total_pages = max(1, -(-total // filters.page_size))

        return SavingsGoalListResponse(
            items=items,
            total=total,
            page=filters.page,
            page_size=filters.page_size,
            total_pages=total_pages,
        )
