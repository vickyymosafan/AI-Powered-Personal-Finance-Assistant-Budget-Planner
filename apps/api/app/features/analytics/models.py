"""
SavingsGoal model — Target tabungan & investment tracking
(placed in analytics as it serves both savings and analytics features)
"""

from __future__ import annotations

import enum
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.models.base import Base, BaseEntity

if TYPE_CHECKING:
    from app.features.auth.models import User


class GoalPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class GoalStatus(str, enum.Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class SavingsGoal(BaseEntity, Base):
    __tablename__ = "savings_goals"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, default=None)

    # Financial targets
    target_amount: Mapped[float] = mapped_column(Float, nullable=False)
    current_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Timeline
    target_date: Mapped["date | None"] = mapped_column(Date, default=None)  # noqa: F821

    # Status & priority
    status: Mapped[GoalStatus] = mapped_column(
        Enum(GoalStatus, name="goal_status"), default=GoalStatus.ACTIVE, nullable=False
    )
    priority: Mapped[GoalPriority] = mapped_column(
        Enum(GoalPriority, name="goal_priority"), default=GoalPriority.MEDIUM, nullable=False
    )

    # AI-generated savings plan
    ai_plan: Mapped[str | None] = mapped_column(Text, default=None)

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="savings_goals")

    @property
    def progress_percentage(self) -> float:
        if self.target_amount == 0:
            return 0.0
        return round((self.current_amount / self.target_amount) * 100, 2)

    @property
    def remaining_amount(self) -> float:
        return max(0.0, self.target_amount - self.current_amount)

    def __repr__(self) -> str:
        return f"<SavingsGoal {self.name}: {self.progress_percentage}%>"
