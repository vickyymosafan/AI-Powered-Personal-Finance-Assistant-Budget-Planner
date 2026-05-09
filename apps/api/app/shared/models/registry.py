"""
Model registry — Imports ALL models for Alembic autogenerate.
Only imported by alembic/env.py to populate Base.metadata.
"""

from app.shared.models.base import Base  # noqa: F401

# Trigger model registration by importing all model modules
from app.features.auth.models import User  # noqa: F401
from app.features.transactions.models import Transaction  # noqa: F401
from app.features.budgets.models import Budget, BudgetItem  # noqa: F401
from app.features.analytics.models import SavingsGoal  # noqa: F401
