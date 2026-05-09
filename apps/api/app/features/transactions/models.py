"""
Transaction model — Income & Expense records
"""

from __future__ import annotations

import enum
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.models.base import Base, BaseEntity

if TYPE_CHECKING:
    from app.features.auth.models import User


class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class TransactionCategory(str, enum.Enum):
    # Income categories
    SALARY = "salary"
    FREELANCE = "freelance"
    INVESTMENT_RETURN = "investment_return"
    OTHER_INCOME = "other_income"

    # Expense categories
    FOOD = "food"
    TRANSPORTATION = "transportation"
    HOUSING = "housing"
    UTILITIES = "utilities"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    INSURANCE = "insurance"
    SAVINGS = "savings"
    DEBT_PAYMENT = "debt_payment"
    OTHER_EXPENSE = "other_expense"


class Transaction(BaseEntity, Base):
    __tablename__ = "transactions"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, name="transaction_type"), nullable=False, index=True
    )
    category: Mapped[TransactionCategory] = mapped_column(
        Enum(TransactionCategory, name="transaction_category"), nullable=False, index=True
    )
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, default=None)
    date: Mapped["date"] = mapped_column(Date, nullable=False, index=True)  # noqa: F821

    # Optional: merchant/source name
    merchant: Mapped[str | None] = mapped_column(String(200), default=None)

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="transactions")

    def __repr__(self) -> str:
        return f"<Transaction {self.type.value} {self.amount} ({self.category.value})>"
