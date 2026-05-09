"""
Transaction feature — Business logic service
Handles CRUD + summary/analytics for transactions.
"""

from collections import defaultdict
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenError, NotFoundError
from app.features.transactions.models import Transaction, TransactionCategory, TransactionType
from app.features.transactions.schemas import (
    CategorySummary,
    CreateTransactionRequest,
    TransactionFilterParams,
    TransactionListResponse,
    TransactionResponse,
    TransactionSummaryResponse,
    UpdateTransactionRequest,
)


def _to_response(tx: Transaction) -> TransactionResponse:
    """Convert Transaction ORM model to response schema."""
    return TransactionResponse(
        id=tx.id,
        type=tx.type.value,
        category=tx.category.value,
        amount=tx.amount,
        description=tx.description,
        date=tx.date.isoformat(),
        merchant=tx.merchant,
        created_at=tx.created_at.isoformat(),
    )


class TransactionService:
    """Stateless transaction service."""

    @staticmethod
    async def create(
        db: AsyncSession, user_id: str, payload: CreateTransactionRequest
    ) -> TransactionResponse:
        """Create a new transaction."""
        tx = Transaction(
            user_id=user_id,
            type=payload.type,
            category=payload.category,
            amount=payload.amount,
            description=payload.description,
            date=payload.date,
            merchant=payload.merchant,
        )
        db.add(tx)
        await db.flush()
        await db.refresh(tx)
        return _to_response(tx)

    @staticmethod
    async def get_by_id(
        db: AsyncSession, user_id: str, transaction_id: str
    ) -> TransactionResponse:
        """Get a single transaction by ID (scoped to user)."""
        tx = await db.get(Transaction, transaction_id)
        if tx is None:
            raise NotFoundError(detail="Transaksi tidak ditemukan")
        if tx.user_id != user_id:
            raise ForbiddenError(detail="Akses ditolak")
        return _to_response(tx)

    @staticmethod
    async def update(
        db: AsyncSession,
        user_id: str,
        transaction_id: str,
        payload: UpdateTransactionRequest,
    ) -> TransactionResponse:
        """Update a transaction (partial update)."""
        tx = await db.get(Transaction, transaction_id)
        if tx is None:
            raise NotFoundError(detail="Transaksi tidak ditemukan")
        if tx.user_id != user_id:
            raise ForbiddenError(detail="Akses ditolak")

        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(tx, field, value)

        await db.flush()
        await db.refresh(tx)
        return _to_response(tx)

    @staticmethod
    async def delete(
        db: AsyncSession, user_id: str, transaction_id: str
    ) -> None:
        """Delete a transaction."""
        tx = await db.get(Transaction, transaction_id)
        if tx is None:
            raise NotFoundError(detail="Transaksi tidak ditemukan")
        if tx.user_id != user_id:
            raise ForbiddenError(detail="Akses ditolak")
        await db.delete(tx)
        await db.flush()

    @staticmethod
    async def list_transactions(
        db: AsyncSession, user_id: str, filters: TransactionFilterParams
    ) -> TransactionListResponse:
        """List transactions with filtering and pagination."""
        # Base query scoped to user
        base = select(Transaction).where(Transaction.user_id == user_id)

        # Apply filters
        if filters.type is not None:
            base = base.where(Transaction.type == filters.type)
        if filters.category is not None:
            base = base.where(Transaction.category == filters.category)
        if filters.start_date is not None:
            base = base.where(Transaction.date >= filters.start_date)
        if filters.end_date is not None:
            base = base.where(Transaction.date <= filters.end_date)
        if filters.min_amount is not None:
            base = base.where(Transaction.amount >= filters.min_amount)
        if filters.max_amount is not None:
            base = base.where(Transaction.amount <= filters.max_amount)

        # Count total
        count_stmt = select(func.count()).select_from(base.subquery())
        total_result = await db.execute(count_stmt)
        total = total_result.scalar() or 0

        # Pagination
        offset = (filters.page - 1) * filters.page_size
        items_stmt = (
            base
            .order_by(Transaction.date.desc(), Transaction.created_at.desc())
            .offset(offset)
            .limit(filters.page_size)
        )
        result = await db.execute(items_stmt)
        items = [_to_response(tx) for tx in result.scalars().all()]

        total_pages = max(1, -(-total // filters.page_size))  # ceil division

        return TransactionListResponse(
            items=items,
            total=total,
            page=filters.page,
            page_size=filters.page_size,
            total_pages=total_pages,
        )

    @staticmethod
    async def get_summary(
        db: AsyncSession,
        user_id: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> TransactionSummaryResponse:
        """Get financial summary with category breakdown."""
        base = select(Transaction).where(Transaction.user_id == user_id)

        if start_date:
            base = base.where(Transaction.date >= start_date)
        if end_date:
            base = base.where(Transaction.date <= end_date)

        result = await db.execute(base)
        transactions = result.scalars().all()

        total_income = 0.0
        total_expense = 0.0
        income_cats: dict[str, dict] = defaultdict(lambda: {"total": 0.0, "count": 0})
        expense_cats: dict[str, dict] = defaultdict(lambda: {"total": 0.0, "count": 0})

        for tx in transactions:
            if tx.type == TransactionType.INCOME:
                total_income += tx.amount
                income_cats[tx.category.value]["total"] += tx.amount
                income_cats[tx.category.value]["count"] += 1
            else:
                total_expense += tx.amount
                expense_cats[tx.category.value]["total"] += tx.amount
                expense_cats[tx.category.value]["count"] += 1

        def _build_summaries(
            cats: dict[str, dict], grand_total: float
        ) -> list[CategorySummary]:
            return sorted(
                [
                    CategorySummary(
                        category=cat,
                        total=round(data["total"], 2),
                        count=data["count"],
                        percentage=round((data["total"] / grand_total) * 100, 2) if grand_total > 0 else 0,
                    )
                    for cat, data in cats.items()
                ],
                key=lambda x: x.total,
                reverse=True,
            )

        return TransactionSummaryResponse(
            total_income=round(total_income, 2),
            total_expense=round(total_expense, 2),
            net_balance=round(total_income - total_expense, 2),
            transaction_count=len(transactions),
            expense_by_category=_build_summaries(expense_cats, total_expense),
            income_by_category=_build_summaries(income_cats, total_income),
            period_start=start_date.isoformat() if start_date else None,
            period_end=end_date.isoformat() if end_date else None,
        )
