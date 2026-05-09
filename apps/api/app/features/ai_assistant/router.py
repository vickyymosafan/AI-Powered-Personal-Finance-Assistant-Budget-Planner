"""
AI Assistant feature — API Router
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user_id
from app.features.ai_assistant.schemas import ChatRequest, ChatResponse
from app.features.ai_assistant.service import AIAssistantService

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """AI chat endpoint — tanya seputar keuangan Anda."""
    return await AIAssistantService.get_chat_reply(db, user_id, payload)


@router.get("/insights", response_model=ChatResponse)
async def get_insights(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """AI financial insights — analisa otomatis profil keuangan Anda."""
    payload = ChatRequest(message="Tolong berikan saya insight dan saran singkat (maksimal 3 poin) mengenai keadaan keuangan saya saat ini.")
    return await AIAssistantService.get_chat_reply(db, user_id, payload)


@router.post("/advice", response_model=ChatResponse)
async def get_advice(
    payload: ChatRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """AI financial advice — sama dengan chat, untuk kompatibilitas endpoint."""
    return await AIAssistantService.get_chat_reply(db, user_id, payload)
