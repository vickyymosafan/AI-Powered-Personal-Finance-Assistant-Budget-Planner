"""
AI Assistant feature — API Router
"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/chat")
async def chat():
    """AI chat endpoint — to be implemented"""
    return {"message": "AI chat endpoint"}


@router.get("/insights")
async def get_insights():
    """AI financial insights — to be implemented"""
    return {"message": "AI insights"}


@router.post("/advice")
async def get_advice():
    """AI financial advice — to be implemented"""
    return {"message": "AI advice"}
