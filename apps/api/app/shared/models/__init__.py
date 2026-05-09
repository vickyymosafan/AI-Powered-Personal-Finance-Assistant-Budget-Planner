"""
Model registry — Import all models so Alembic can detect them.
This module MUST be imported before running migrations.
"""

from app.shared.models.base import Base, BaseEntity, TimestampMixin  # noqa: F401

# Feature models
from app.features.auth.models import User  # noqa: F401
from app.features.transactions.models import (  # noqa: F401
    Transaction,
    TransactionCategory,
    TransactionType,
)
from app.features.budgets.models import Budget, BudgetItem, BudgetPeriod  # noqa: F401
from app.features.analytics.models import (  # noqa: F401
    GoalPriority,
    GoalStatus,
    SavingsGoal,
)

__all__ = [
    "Base",
    "BaseEntity",
    "TimestampMixin",
    "User",
    "Transaction",
    "TransactionType",
    "TransactionCategory",
    "Budget",
    "BudgetItem",
    "BudgetPeriod",
    "SavingsGoal",
    "GoalPriority",
    "GoalStatus",
]
