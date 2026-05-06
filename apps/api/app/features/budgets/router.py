"""
Budgets feature — API Router
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_budgets():
    """List budgets — to be implemented"""
    return {"message": "List budgets"}


@router.post("/")
async def create_budget():
    """Create budget — to be implemented"""
    return {"message": "Create budget"}


@router.get("/{budget_id}")
async def get_budget(budget_id: str):
    """Get budget by ID — to be implemented"""
    return {"message": f"Get budget {budget_id}"}


@router.put("/{budget_id}")
async def update_budget(budget_id: str):
    """Update budget — to be implemented"""
    return {"message": f"Update budget {budget_id}"}


@router.delete("/{budget_id}")
async def delete_budget(budget_id: str):
    """Delete budget — to be implemented"""
    return {"message": f"Delete budget {budget_id}"}


@router.get("/progress")
async def get_progress():
    """Get budget progress — to be implemented"""
    return {"message": "Budget progress"}
