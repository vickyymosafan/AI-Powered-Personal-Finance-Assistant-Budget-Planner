"""
Analytics feature — Business logic service
Handles CRUD operations for Savings Goals and analytics logic.
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenError, NotFoundError
from app.features.analytics.models import SavingsGoal
from app.features.analytics.schemas import (
    AnalyticsOverviewResponse,
    CategoriesResponse,
    CategoryDataPoint,
    CreateSavingsGoalRequest,
    SavingsGoalFilterParams,
    SavingsGoalListResponse,
    SavingsGoalResponse,
    TrendDataPoint,
    TrendsResponse,
    UpdateSavingsGoalRequest,
)
from app.features.transactions.models import Transaction, TransactionType


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


class AnalyticsService:
    """Service to handle high-level analytics operations."""

    @staticmethod
    async def get_overview(db: AsyncSession, user_id: str) -> AnalyticsOverviewResponse:
        """Get high-level overview: total income, expense, and goal counts."""
        # Get total income and expense
        stmt_transactions = (
            select(Transaction.type, func.sum(Transaction.amount))
            .where(Transaction.user_id == user_id)
            .group_by(Transaction.type)
        )
        result_tx = await db.execute(stmt_transactions)
        
        total_income = 0.0
        total_expense = 0.0
        for tx_type, total in result_tx:
            if tx_type == TransactionType.INCOME:
                total_income = total or 0.0
            elif tx_type == TransactionType.EXPENSE:
                total_expense = total or 0.0
                
        # Get goal counts
        stmt_goals = (
            select(SavingsGoal.status, func.count(SavingsGoal.id))
            .where(SavingsGoal.user_id == user_id)
            .group_by(SavingsGoal.status)
        )
        result_goals = await db.execute(stmt_goals)
        
        active_goals = 0
        completed_goals = 0
        for status, count in result_goals:
            if status.value == "active":
                active_goals = count
            elif status.value == "completed":
                completed_goals = count

        return AnalyticsOverviewResponse(
            total_income=total_income,
            total_expense=total_expense,
            net_balance=total_income - total_expense,
            active_goals_count=active_goals,
            completed_goals_count=completed_goals,
        )

    @staticmethod
    async def get_spending_categories(
        db: AsyncSession, user_id: str, year: int, month: int
    ) -> CategoriesResponse:
        """Break down expenses by category for a given month."""
        from calendar import monthrange
        import datetime
        
        _, last_day = monthrange(year, month)
        start_date = datetime.date(year, month, 1)
        end_date = datetime.date(year, month, last_day)

        stmt = (
            select(Transaction.category, func.sum(Transaction.amount))
            .where(
                Transaction.user_id == user_id,
                Transaction.type == TransactionType.EXPENSE,
                Transaction.date >= start_date,
                Transaction.date <= end_date,
            )
            .group_by(Transaction.category)
        )
        
        result = await db.execute(stmt)
        categories_data = result.all()
        
        total_expense = sum(amount for _, amount in categories_data) if categories_data else 0.0
        
        points = []
        for category, amount in categories_data:
            cat_name = category.value if hasattr(category, "value") else str(category)
            pct = round((amount / total_expense) * 100, 2) if total_expense > 0 else 0.0
            points.append(CategoryDataPoint(category=cat_name, amount=amount or 0.0, percentage=pct))
            
        points.sort(key=lambda x: x.amount, reverse=True)
        return CategoriesResponse(categories=points)

    @staticmethod
    async def get_trends(
        db: AsyncSession, user_id: str, year: int
    ) -> TrendsResponse:
        """Get monthly income vs expense trends for a specific year."""
        import datetime
        
        start_date = datetime.date(year, 1, 1)
        end_date = datetime.date(year, 12, 31)

        stmt = (
            select(
                func.extract("month", Transaction.date).label("month"),
                Transaction.type,
                func.sum(Transaction.amount).label("total")
            )
            .where(
                Transaction.user_id == user_id,
                Transaction.date >= start_date,
                Transaction.date <= end_date,
            )
            .group_by("month", Transaction.type)
        )
        
        result = await db.execute(stmt)
        
        # Initialize 12 months data
        monthly_data = {m: {"income": 0.0, "expense": 0.0} for m in range(1, 13)}
        
        for row in result:
            month = int(row.month)
            tx_type = row.type
            amount = row.total or 0.0
            
            if tx_type == TransactionType.INCOME:
                monthly_data[month]["income"] += amount
            elif tx_type == TransactionType.EXPENSE:
                monthly_data[month]["expense"] += amount
                
        trends = []
        for m in range(1, 13):
            period_str = f"{year}-{m:02d}"
            trends.append(
                TrendDataPoint(
                    period=period_str,
                    income=monthly_data[m]["income"],
                    expense=monthly_data[m]["expense"]
                )
            )
            
        return TrendsResponse(trends=trends)
