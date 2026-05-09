"""
Budgets feature — Business logic service
Handles CRUD operations for Budget and BudgetItem.
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import ForbiddenError, NotFoundError
from app.features.budgets.models import Budget, BudgetItem
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


def _item_to_response(item: BudgetItem) -> BudgetItemResponse:
    return BudgetItemResponse(
        id=item.id,
        budget_id=item.budget_id,
        category=item.category,
        allocated_amount=item.allocated_amount,
        spent_amount=item.spent_amount,
        ai_recommendation=item.ai_recommendation,
        remaining=item.remaining,
        usage_percentage=item.usage_percentage,
        created_at=item.created_at.isoformat(),
    )


def _budget_to_response(budget: Budget) -> BudgetResponse:
    return BudgetResponse(
        id=budget.id,
        name=budget.name,
        period=budget.period.value,
        year=budget.year,
        month=budget.month,
        total_income=budget.total_income,
        total_budget=budget.total_budget,
        ai_notes=budget.ai_notes,
        items=[_item_to_response(i) for i in budget.items],
        created_at=budget.created_at.isoformat(),
    )


class BudgetService:
    """Stateless budget service."""

    @staticmethod
    async def create(
        db: AsyncSession, user_id: str, payload: CreateBudgetRequest
    ) -> BudgetResponse:
        """Create a new budget with nested items."""
        budget = Budget(
            user_id=user_id,
            name=payload.name,
            period=payload.period,
            year=payload.year,
            month=payload.month,
            total_income=payload.total_income,
            total_budget=payload.total_budget,
            ai_notes=payload.ai_notes,
        )
        
        for item_payload in payload.items:
            budget.items.append(
                BudgetItem(
                    category=item_payload.category,
                    allocated_amount=item_payload.allocated_amount,
                    spent_amount=item_payload.spent_amount,
                    ai_recommendation=item_payload.ai_recommendation,
                )
            )

        db.add(budget)
        await db.flush()
        await db.refresh(budget)
        return _budget_to_response(budget)

    @staticmethod
    async def get_by_id(
        db: AsyncSession, user_id: str, budget_id: str
    ) -> BudgetResponse:
        """Get a single budget by ID."""
        budget = await db.get(Budget, budget_id)
        if budget is None:
            raise NotFoundError(detail="Budget tidak ditemukan")
        if budget.user_id != user_id:
            raise ForbiddenError(detail="Akses ditolak")
        return _budget_to_response(budget)

    @staticmethod
    async def update(
        db: AsyncSession, user_id: str, budget_id: str, payload: UpdateBudgetRequest
    ) -> BudgetResponse:
        """Update a budget (partial update). Does not modify items."""
        budget = await db.get(Budget, budget_id)
        if budget is None:
            raise NotFoundError(detail="Budget tidak ditemukan")
        if budget.user_id != user_id:
            raise ForbiddenError(detail="Akses ditolak")

        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(budget, field, value)

        await db.flush()
        await db.refresh(budget)
        return _budget_to_response(budget)

    @staticmethod
    async def delete(db: AsyncSession, user_id: str, budget_id: str) -> None:
        """Delete a budget."""
        budget = await db.get(Budget, budget_id)
        if budget is None:
            raise NotFoundError(detail="Budget tidak ditemukan")
        if budget.user_id != user_id:
            raise ForbiddenError(detail="Akses ditolak")
        await db.delete(budget)
        await db.flush()

    @staticmethod
    async def list_budgets(
        db: AsyncSession, user_id: str, filters: BudgetFilterParams
    ) -> BudgetListResponse:
        """List budgets with filtering and pagination."""
        base = select(Budget).where(Budget.user_id == user_id)

        if filters.year is not None:
            base = base.where(Budget.year == filters.year)
        if filters.month is not None:
            base = base.where(Budget.month == filters.month)
        if filters.period is not None:
            base = base.where(Budget.period == filters.period)

        # Count
        count_stmt = select(func.count()).select_from(base.subquery())
        total = (await db.execute(count_stmt)).scalar() or 0

        # Pagination
        offset = (filters.page - 1) * filters.page_size
        items_stmt = (
            base.order_by(Budget.year.desc(), Budget.month.desc())
            .offset(offset)
            .limit(filters.page_size)
        )
        result = await db.execute(items_stmt)
        items = [_budget_to_response(b) for b in result.scalars().all()]

        total_pages = max(1, -(-total // filters.page_size))

        return BudgetListResponse(
            items=items,
            total=total,
            page=filters.page,
            page_size=filters.page_size,
            total_pages=total_pages,
        )

    # ── BudgetItem Specific Methods ─────────────────────────────────

    @staticmethod
    async def add_item(
        db: AsyncSession, user_id: str, budget_id: str, payload: BudgetItemCreate
    ) -> BudgetItemResponse:
        """Add a single item to an existing budget."""
        budget = await db.get(Budget, budget_id)
        if budget is None:
            raise NotFoundError(detail="Budget tidak ditemukan")
        if budget.user_id != user_id:
            raise ForbiddenError(detail="Akses ditolak")

        item = BudgetItem(
            budget_id=budget_id,
            category=payload.category,
            allocated_amount=payload.allocated_amount,
            spent_amount=payload.spent_amount,
            ai_recommendation=payload.ai_recommendation,
        )
        db.add(item)
        await db.flush()
        await db.refresh(item)
        return _item_to_response(item)

    @staticmethod
    async def update_item(
        db: AsyncSession, user_id: str, item_id: str, payload: BudgetItemUpdate
    ) -> BudgetItemResponse:
        """Update a specific budget item."""
        stmt = select(BudgetItem).options(selectinload(BudgetItem.budget)).where(BudgetItem.id == item_id)
        result = await db.execute(stmt)
        item = result.scalar_one_or_none()

        if item is None:
            raise NotFoundError(detail="Budget item tidak ditemukan")
        if item.budget.user_id != user_id:
            raise ForbiddenError(detail="Akses ditolak")

        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(item, field, value)

        await db.flush()
        await db.refresh(item)
        return _item_to_response(item)

    @staticmethod
    async def delete_item(db: AsyncSession, user_id: str, item_id: str) -> None:
        """Delete a specific budget item."""
        stmt = select(BudgetItem).options(selectinload(BudgetItem.budget)).where(BudgetItem.id == item_id)
        result = await db.execute(stmt)
        item = result.scalar_one_or_none()

        if item is None:
            raise NotFoundError(detail="Budget item tidak ditemukan")
        if item.budget.user_id != user_id:
            raise ForbiddenError(detail="Akses ditolak")

        await db.delete(item)
        await db.flush()
