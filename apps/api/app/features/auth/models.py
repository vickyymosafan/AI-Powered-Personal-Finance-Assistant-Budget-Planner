"""
User model — Authentication & profile
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.models.base import Base, BaseEntity

if TYPE_CHECKING:
    from app.features.analytics.models import SavingsGoal
    from app.features.budgets.models import Budget
    from app.features.transactions.models import Transaction


class User(BaseEntity, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Currency preference (ISO 4217)
    currency: Mapped[str] = mapped_column(String(3), default="IDR", nullable=False)

    # Monthly income for budget calculations
    monthly_income: Mapped[float | None] = mapped_column(default=None)

    # Relationships
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    budgets: Mapped[list["Budget"]] = relationship(
        "Budget", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    savings_goals: Mapped[list["SavingsGoal"]] = relationship(
        "SavingsGoal", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<User {self.email}>"
