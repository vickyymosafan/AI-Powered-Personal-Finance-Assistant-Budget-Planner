"""
AI Assistant feature — Service
Generates context-aware financial advice using Gemini.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.llm import get_financial_advice_async
from app.features.ai_assistant.schemas import ChatRequest, ChatResponse
from app.features.analytics.service import AnalyticsService


class AIAssistantService:
    """Service to handle AI Chat interactions."""

    @staticmethod
    async def get_chat_reply(
        db: AsyncSession, user_id: str, request: ChatRequest
    ) -> ChatResponse:
        """
        Generate AI reply based on user message and financial context.
        """
        # Fetch high-level context
        overview = await AnalyticsService.get_overview(db, user_id)
        
        # Build prompt with context
        system_prompt = f"""Kamu adalah AI Financial Advisor profesional yang ramah dan ahli dalam mengelola keuangan pribadi.
Kamu sedang berbicara dengan seorang pengguna. Berikut adalah ringkasan keuangan mereka saat ini:
- Total Pemasukan: Rp {overview.total_income:,.2f}
- Total Pengeluaran: Rp {overview.total_expense:,.2f}
- Sisa Saldo (Net Balance): Rp {overview.net_balance:,.2f}
- Target Tabungan Aktif: {overview.active_goals_count}

Aturan:
1. Berikan jawaban yang praktis, ringkas, dan dapat langsung diterapkan.
2. Gunakan bahasa Indonesia yang santai tapi profesional.
3. Jangan mengulangi data keuangan di atas kecuali relevan dengan pertanyaan pengguna.
4. Fokus pada menjawab pertanyaan spesifik pengguna.
"""
        
        full_prompt = f"{system_prompt}\n\nPertanyaan Pengguna: {request.message}\nJawaban AI:"
        
        reply_text = await get_financial_advice_async(full_prompt)
        
        return ChatResponse(reply=reply_text)
