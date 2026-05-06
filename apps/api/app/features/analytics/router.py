"""
Analytics feature — API Router
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/overview")
async def get_overview():
    """Get analytics overview — to be implemented"""
    return {"message": "Analytics overview"}


@router.get("/spending")
async def get_spending():
    """Get spending analytics — to be implemented"""
    return {"message": "Spending analytics"}


@router.get("/trends")
async def get_trends():
    """Get trend analytics — to be implemented"""
    return {"message": "Trend analytics"}


@router.get("/categories")
async def get_categories():
    """Get category analytics — to be implemented"""
    return {"message": "Category analytics"}
