"""
Budget model — Monthly budget plans per category
"""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.models.base import Base, BaseEntity

if TYPE_CHECKING:
    from app.features.auth.models import User


class BudgetPeriod(str, enum.Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class Budget(BaseEntity, Base):
    __tablename__ = "budgets"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    period: Mapped[BudgetPeriod] = mapped_column(
        Enum(BudgetPeriod, name="budget_period"), default=BudgetPeriod.MONTHLY, nullable=False
    )

    # Budget year/month target
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    month: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    # Amounts
    total_income: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_budget: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # AI-generated allocation notes
    ai_notes: Mapped[str | None] = mapped_column(Text, default=None)

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="budgets")
    items: Mapped[list["BudgetItem"]] = relationship(
        "BudgetItem", back_populates="budget", cascade="all, delete-orphan", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Budget {self.name} ({self.year}-{self.month:02d})>"


class BudgetItem(BaseEntity, Base):
    __tablename__ = "budget_items"

    budget_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("budgets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    allocated_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    spent_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # AI recommendation for this category
    ai_recommendation: Mapped[str | None] = mapped_column(Text, default=None)

    # Relationship
    budget: Mapped["Budget"] = relationship("Budget", back_populates="items")

    @property
    def remaining(self) -> float:
        return self.allocated_amount - self.spent_amount

    @property
    def usage_percentage(self) -> float:
        if self.allocated_amount == 0:
            return 0.0
        return round((self.spent_amount / self.allocated_amount) * 100, 2)

    def __repr__(self) -> str:
        return f"<BudgetItem {self.category}: {self.allocated_amount}>"
