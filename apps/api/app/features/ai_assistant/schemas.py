"""
AI Assistant feature — Pydantic schemas
"""

from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., max_length=1000)
    context_type: Optional[str] = Field(default="general", description="Bisa 'general', 'budget', 'savings', atau 'spending'")


class ChatResponse(BaseModel):
    reply: str
    tokens_used: Optional[int] = None
