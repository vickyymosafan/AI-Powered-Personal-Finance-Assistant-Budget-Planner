"""
Transactions feature — API Router
Full CRUD + summary with filtering, pagination, and auth guard.
"""

from datetime import date as DateType
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user_id
from app.features.transactions.models import TransactionCategory, TransactionType
from app.features.transactions.schemas import (
    CreateTransactionRequest,
    TransactionFilterParams,
    TransactionListResponse,
    TransactionResponse,
    TransactionSummaryResponse,
    UpdateTransactionRequest,
)
from app.features.transactions.service import TransactionService

router = APIRouter()


# ── Summary (placed before /{id} to avoid path conflict) ────────


@router.get("/summary", response_model=TransactionSummaryResponse)
async def get_summary(
    start_date: Optional[DateType] = Query(default=None, description="Filter mulai tanggal"),
    end_date: Optional[DateType] = Query(default=None, description="Filter sampai tanggal"),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Ringkasan keuangan: total income/expense, net balance, breakdown per kategori."""
    return await TransactionService.get_summary(db, user_id, start_date, end_date)


# ── CRUD Endpoints ──────────────────────────────────────────────


@router.get("/", response_model=TransactionListResponse)
async def list_transactions(
    type: TransactionType | None = Query(default=None),
    category: TransactionCategory | None = Query(default=None),
    start_date: Optional[DateType] = Query(default=None),
    end_date: Optional[DateType] = Query(default=None),
    min_amount: float | None = Query(default=None, ge=0),
    max_amount: float | None = Query(default=None, ge=0),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """List transaksi dengan filter, sort (terbaru), dan pagination."""
    filters = TransactionFilterParams(
        type=type,
        category=category,
        start_date=start_date,
        end_date=end_date,
        min_amount=min_amount,
        max_amount=max_amount,
        page=page,
        page_size=page_size,
    )
    return await TransactionService.list_transactions(db, user_id, filters)


@router.post("/", response_model=TransactionResponse, status_code=201)
async def create_transaction(
    payload: CreateTransactionRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Catat transaksi baru (income/expense)."""
    return await TransactionService.create(db, user_id, payload)


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Ambil detail satu transaksi."""
    return await TransactionService.get_by_id(db, user_id, transaction_id)


@router.patch("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: str,
    payload: UpdateTransactionRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Update transaksi (partial update)."""
    return await TransactionService.update(db, user_id, transaction_id, payload)


@router.delete("/{transaction_id}", status_code=204)
async def delete_transaction(
    transaction_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Hapus transaksi."""
    await TransactionService.delete(db, user_id, transaction_id)
